# Document Tutor

A simple document Q&A app built with Python, Streamlit, SQLite, and OpenRouter. Upload PDF, TXT, or Markdown files to retrieve relevant passages and optionally generate AI answers grounded in your documents.

## Features

- Upload PDF, TXT, and Markdown files.
- Index document text locally in SQLite.
- Retrieve relevant passages using TF-IDF.
- Generate answers using an OpenRouter model.
- Search documents without an API key.

## Setup

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Create a `.env` file next to `app.py`:

```env
OPENROUTER_API_KEY=your_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=minimax/minimax-m3.1-flash:free
```

Get a key from [OpenRouter](https://openrouter.ai/). Free model availability and rate limits may change.

## Usage

1. Upload your documents.
2. Click **Index documents**.
3. Enter a question and click **Search documents**.
4. Review retrieved passages and the AI answer, if configured.

## Privacy

- Never upload `.env` to GitHub; it may contain your API key.
- Keep `tutor_data.db` out of GitHub. It stores indexed document text, so keep your local copy if you want to preserve your index.
- Add `.env.example` with empty credentials for other developers.
- If a key was committed or exposed, revoke it and create a new one.

Ensure `.gitignore` includes:

```gitignore
.env
.env.*
!.env.example
tutor_data.db
.venv/
venv/
__pycache__/
*.py[cod]
.vscode/
```

## Project Structure

```text
app.py
requirements.txt
README.md
LICENSE
.env.example
.gitignore
tutor/
```
