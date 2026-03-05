from ingest import ingest_documents
import streamlit as st
import os
from src.qa_chain import get_qa_chain

st.set_page_config(
    page_title="HR Assistant",
    page_icon="🧳",
    layout="wide"
)

# --------------------------
# Sidebar
# --------------------------

st.sidebar.title("🧳 HR Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

# --------------------------
# Dashboard
# --------------------------

if page == "Dashboard":
    st.title("🧳 HR Assistant Dashboard")
    st.write("AI powered HR helpdesk for employees")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Employees", "120")
    col2.metric("HR Policies", "15")
    col3.metric("Announcements", "3")
    col4.metric("HR Queries Today", "27")

    st.divider()

    st.subheader("📢 Latest HR Updates")
    st.write("• Annual appraisal cycle begins next month")
    st.write("• New work from home policy updated")
    st.write("• Health insurance benefits revised")

# --------------------------
# HR Chatbot
# --------------------------

elif page == "HR Chatbot":
    st.title("💬 HR Chatbot")
    st.write("Ask me anything about HR policies!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Ask about HR policies...")

    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Get response  ✅ FIX: pass string directly, not {"query": ...}
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    qa_chain = get_qa_chain()
                    response = qa_chain.invoke(str(user_input))  # ✅ FIXED LINE
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --------------------------
# Upload Documents
# --------------------------

elif page == "Upload Documents":
    st.title("📄 Upload HR Documents")

    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            try:
                temp_path = f"docs/{uploaded_file.name}"
                os.makedirs("docs", exist_ok=True)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                ingest_documents()
                st.success("Document uploaded and processed successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# --------------------------
# About
# --------------------------

elif page == "About":
    st.title("ℹ️ About HR Assistant")
    st.write("""
    This HR Assistant is powered by AI to help employees quickly find answers 
    to HR-related questions based on company documents and policies.
    
    **Technologies used:**
    - Streamlit
    - LangChain
    - Groq (Llama 3.3)
    - FAISS Vector Store
    - HuggingFace Embeddings
    """)