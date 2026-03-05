from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_documents(docs_folder='docs'):
    all_docs = []
    for filename in os.listdir(docs_folder):
        if filename.endswith('.pdf'):
            filepath = os.path.join(docs_folder, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            all_docs.extend(docs)
            print(f'Loaded: {filename} ({len(docs)} pages)')
    return all_docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)
    print(f'Split into {len(chunks)} chunks')
    return chunks