import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=False)

def chat_completion(messages):
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip() or os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(f"No API key loaded. Check {PROJECT_ROOT / '.env'}")
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1").strip()
    model = os.getenv("LLM_MODEL", "minimax/minimax-m3.1-flash:free").strip()
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return response.choices[0].message.content or ""
