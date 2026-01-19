
import pickle
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings

VECTOR_DB = "vector_store.pkl"

def search_docs(query, top_k=3):
    with open(VECTOR_DB, "rb") as f:
        index, chunks = pickle.load(f)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    q_vec = np.array(embeddings.embed_query(query)).reshape(1, -1)

    _, idxs = index.search(q_vec, top_k)
    return [chunks[i].page_content for i in idxs[0]]
