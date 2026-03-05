from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

VECTORSTORE_PATH = "vectorstore"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore(chunks):

    clean_chunks = []

    for chunk in chunks:

        if hasattr(chunk, "page_content"):

            text = chunk.page_content

            if isinstance(text, str):

                text = text.strip()

                if text != "":
                    chunk.page_content = text.replace("\n", " ")
                    clean_chunks.append(chunk)

    print("Valid chunks:", len(clean_chunks))

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        documents=clean_chunks,
        embedding=embeddings
    )

    vectorstore.save_local(VECTORSTORE_PATH)

    print("Vectorstore created")

    return vectorstore


def load_vectorstore():

    embeddings = get_embeddings()

    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )