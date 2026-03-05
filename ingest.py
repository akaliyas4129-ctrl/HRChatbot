import os
from src.document_loader import load_documents
from src.vector_store import create_vectorstore

def ingest_documents():

    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    print("Creating vectorstore...")

    vectorstore = create_vectorstore(documents)

    print("Vectorstore created successfully")

    return vectorstore


if __name__ == "__main__":
    ingest_documents()