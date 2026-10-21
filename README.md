# Document Tutor

A lightweight document-first AI study assistant. Upload PDF, TXT, or Markdown files, index their contents locally, and ask questions to retrieve relevant passages. With an OpenRouter API key configured, the app can also generate answers grounded in the retrieved text.

## Features

- Upload PDF, TXT, and Markdown documents.
- Extract and chunk document text.
- Store indexed passages locally in SQLite.
- Retrieve relevant passages using TF-IDF similarity.
- Generate answers using an OpenRouter-compatible LLM API.
- Search indexed documents without an API key.
- Display source filenames for retrieved passages.
- Use a simple Streamlit web interface.

## Tech Stack

- **Python** — application logic
- **Streamlit** — web interface
- **SQLite** — local document index
- **scikit-learn** — TF-IDF retrieval
- **PyPDF** — PDF text extraction
- **OpenAI Python SDK** — OpenAI-compatible API client
- **OpenRouter** — hosted model API
- **MiniMax M3.1 Flash Free** — configurable default model route

## How It Works

1. Upload PDF, TXT, or Markdown files.
2. Extract text and split it into smaller chunks.
3. Store the chunks in a local SQLite database.
4. Search the indexed content using TF-IDF similarity.
5. Display the most relevant passages.
6. If an API key is configured, send the question and retrieved passages to the selected LLM to generate an answer.

TF-IDF is a lightweight keyword-based retrieval method. It does not provide the same semantic understanding as embedding-based search.

## Requirements

- Python 3.10 or newer
- An OpenRouter API key for AI-generated answers
- Internet access for dependency installation and model API requests

Document retrieval works without an API key; generated answers require a working model configuration.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL with your repository URL.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root, next to `app.py`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=minimax/minimax-m3.1-flash:free
```

Get an API key from [OpenRouter](https://openrouter.ai/). Keep it private and never commit `.env` to GitHub. Model availability, free-tier limits, and rate limits are controlled by the provider and may change.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Usage

1. Upload your files in the sidebar.
2. Select **Index documents**.
3. Enter a question in the retrieval section.
4. Select **Search documents**.
5. Review the retrieved passages and source filenames.
6. If the API is configured, review the generated answer.

Example questions:

- Summarize the key concepts in these notes.
- Explain gradient descent in simple terms.
- Find the section that describes data ingestion.
- Give examples of the concepts covered in this document.

## Project Structure

```text
document-tutor/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tutor/
    ├── __init__.py
    ├── llm.py
    ├── memory.py
    └── retrieval.py
```

The app creates `tutor_data.db` locally when it runs. Keep this database out of version control because it contains indexed document text.

## Privacy and Limitations

- Indexed document chunks are stored locally in `tutor_data.db`.
- When AI answers are enabled, your question and retrieved passages are sent to the configured model provider.
- Do not upload confidential material unless you have permission and understand the provider's data-handling terms.
- Scanned PDFs may require OCR because they may not contain extractable text.
- TF-IDF retrieval is keyword-based and may miss relevant passages when the wording differs.
- AI-generated answers can be incorrect. Verify important information against the original documents.
- This is an educational prototype, not a production-ready multi-user service.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
