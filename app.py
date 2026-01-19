
import os
from fastapi import FastAPI
from pydantic import BaseModel
from retrieval import search_docs
from llm import generate_answer

app = FastAPI(title="Chat With Your Docs")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    docs = search_docs(query.question)
    answer = generate_answer(query.question, docs)
    return {"answer": answer, "sources": docs}
