import re
import sqlite3
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DB_PATH = Path(__file__).resolve().parent.parent / "tutor_data.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _chunks(text, size=1000, overlap=160):
    text = re.sub(r"\s+", " ", text).strip()
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def _ensure_table():
    with _connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL, chunk TEXT NOT NULL)""")

def add_documents(documents):
    _ensure_table()
    added = 0
    with _connect() as c:
        for filename, text in documents:
            # Replace prior indexed chunks for this filename to avoid duplicates.
            c.execute("DELETE FROM documents WHERE filename = ?", (filename,))
            for chunk in _chunks(text):
                c.execute("INSERT INTO documents(filename, chunk) VALUES(?, ?)", (filename, chunk))
                added += 1
    return added

def list_documents():
    _ensure_table()
    with _connect() as c:
        rows = c.execute("SELECT DISTINCT filename FROM documents ORDER BY filename").fetchall()
    return [r["filename"] for r in rows]

def clear_documents():
    _ensure_table()
    with _connect() as c:
        c.execute("DELETE FROM documents")

def retrieve_context(query, limit=8):
    _ensure_table()
    with _connect() as c:
        rows = c.execute("SELECT filename, chunk FROM documents").fetchall()
    if not rows:
        return ""
    texts = [r["chunk"] for r in rows]
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(texts + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    except ValueError:
        return ""
    best = scores.argsort()[::-1][:limit]
    selected = []
    for i in best:
        if scores[i] > 0:
            selected.append(f"**Source: {rows[i]['filename']}** (relevance {scores[i]:.2f})\n\n> {texts[i]}")
    return "\n\n---\n\n".join(selected)
