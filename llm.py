
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(question, docs):
    context = "\n\n".join(docs)
    prompt = f"Answer the question based only on the context.\n\nContext:\n{context}\n\nQuestion: {question}"

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)
    return r.json().get("response", "")
