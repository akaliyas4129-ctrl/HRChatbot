from src.document_loader import load_documents, split_documents
from src.vector_store import create_vectorstore

print('Loading documents...')
docs = load_documents()

print('Splitting documents...')
chunks = split_documents(docs)

print('Creating vector store...')
vectorstore = create_vectorstore(chunks)

print('Done! All documents indexed successfully.')
