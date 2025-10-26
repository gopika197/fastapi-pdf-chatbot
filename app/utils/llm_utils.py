import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = os.getenv(
    "HF_MODEL_URL",
    "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
)

def ask_llm(context: str, question: str) -> str:
    """
    Call Hugging Face QA model
    """
    if not HF_API_KEY or not HF_API_URL:
        return "LLM error: HF_API_KEY or HF_API_URL not set"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": {
            "question": question,
            "context": context[:30000]
        }
    }

    try:
        resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "answer" in data:
            return data["answer"].strip()
        return str(data)
    except Exception as e:
        return f"LLM error: {e}"

