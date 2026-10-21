import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import os
from tutor.retrieval import add_documents, retrieve_context, list_documents, clear_documents
from tutor.llm import chat_completion

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

st.set_page_config(page_title="Document Tutor", page_icon="📚", layout="wide")
st.title("📚 Document Tutor")
st.write("Upload your documents, ask questions, and retrieve answers grounded in your files.")
st.info("This version focuses on document upload and retrieval. It does not require chat history or a learning profile.")

with st.sidebar:
    st.header("1. Upload documents")
    uploads = st.file_uploader(
        "Choose PDF, TXT, or Markdown files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
    )
    if st.button("Index documents", type="primary", use_container_width=True, disabled=not uploads):
        documents = []
        errors = []
        for file in uploads:
            try:
                if file.name.lower().endswith(".pdf"):
                    from pypdf import PdfReader
                    import io
                    reader = PdfReader(io.BytesIO(file.getvalue()))
                    content = "\n".join(page.extract_text() or "" for page in reader.pages)
                else:
                    content = file.getvalue().decode("utf-8", errors="ignore")
                if content.strip():
                    documents.append((file.name, content))
                else:
                    errors.append(f"{file.name}: no extractable text found")
            except Exception as e:
                errors.append(f"{file.name}: {e}")
        if documents:
            count = add_documents(documents)
            st.success(f"Indexed {count} text chunks from {len(documents)} file(s).")
        for error in errors:
            st.warning(error)

    indexed = list_documents()
    st.caption(f"{len(indexed)} document(s) indexed in the local database.")
    if indexed:
        with st.expander("Indexed documents", expanded=True):
            for filename in indexed:
                st.write(f"• {filename}")
        if st.button("Clear indexed documents", use_container_width=True):
            clear_documents()
            st.success("Indexed document store cleared.")
            st.rerun()

st.divider()
st.header("2. Retrieve information")
question = st.text_area(
    "What do you want to find in your documents?",
    placeholder="Example: Explain all the concepts covered in these notes, with simple examples.",
    height=100,
)
col1, col2 = st.columns([1, 4])
with col1:
    ask = st.button("Search documents", type="primary", use_container_width=True)
with col2:
    st.caption("Answers use matching passages from your indexed files. For AI-generated explanations, configure an API key in `.env`.")

if ask:
    if not question.strip():
        st.warning("Enter a question first.")
    elif not list_documents():
        st.warning("Upload and index at least one document in the sidebar first.")
    else:
        with st.spinner("Searching your documents..."):
            context = retrieve_context(question, limit=8)
        if not context:
            st.warning("No sufficiently relevant passages found. Try different keywords or check that the document contains extractable text.")
        else:
            st.subheader("Retrieved passages")
            st.markdown(context)
            api_key = os.getenv("OPENROUTER_API_KEY", "").strip() or os.getenv("OPENAI_API_KEY", "").strip()
            if api_key:
                st.subheader("Answer based on your documents")
                try:
                    answer = chat_completion([
                        {"role": "system", "content": """Answer the user's question using only the retrieved document passages below. If the passages do not contain enough information, say so clearly. Explain concepts simply and cite the source filename provided in the context. Do not invent facts."""},
                        {"role": "user", "content": f"Question: {question}\n\nRetrieved passages:\n{context}"}
                    ])
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"LLM request failed: {e}")
                    st.caption("The retrieved passages are still available above. Check the model ID, API key, OpenRouter credits/rate limits, and network connection.")
            else:
                st.warning("No API key was loaded, so only document retrieval is available. Add OPENROUTER_API_KEY to the project-root .env file and restart Streamlit to enable generated answers.")

st.divider()
st.caption("Privacy: document text and the local index stay on your computer. When AI answers are enabled, retrieved passages and your question are sent to your configured model provider.")
