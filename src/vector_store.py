from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

VECTORSTORE_PATH = 'vectorstore'

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2'
    )

def create_vectorstore(chunks):

    # remove empty chunks
    clean_chunks = []

    for chunk in chunks:
        if chunk.page_content and isinstance(chunk.page_content, str):
            clean_chunks.append(chunk)

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        documents=clean_chunks,
        embedding=embeddings
    )

    vectorstore.save_local(VECTORSTORE_PATH)

    print(f"Vectorstore created with {len(clean_chunks)} chunks")

    return vectorstore
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f'Vectorstore created with {len(chunks)} chunks')
    return vectorstore

def load_vectorstore():
    embeddings = get_embeddings()
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )