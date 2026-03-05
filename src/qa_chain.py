from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.vector_store import load_vectorstore
import os
from dotenv import load_dotenv

load_dotenv()

PROMPT_TEMPLATE = """
You are a helpful HR assistant for new employees.
Use ONLY the context below to answer the question.
If the answer is not in the context, say:
'I don't have that information in the HR documents. Please contact HR directly.'

Context: {context}

Question: {question}

Helpful Answer:"""

def get_qa_chain():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=['context', 'question']
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain