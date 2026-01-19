
import os, argparse
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import faiss
import pickle

VECTOR_DB = "vector_store.pkl"

def load_docs(path):
    docs = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(full_path)
        else:
            loader = TextLoader(full_path)
        docs.extend(loader.load())
    return docs

def build_index(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectors = embeddings.embed_documents([c.page_content for c in chunks])

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)

    with open(VECTOR_DB, "wb") as f:
        pickle.dump((index, chunks), f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", required=True)
    args = parser.parse_args()

    docs = load_docs(args.docs)
    build_index(docs)
    print("Ingestion complete. Vector store saved.")
