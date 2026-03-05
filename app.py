import streamlit as st
import os
from src.qa_chain import get_qa_chain
from ingest import ingest_documents

st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="wide"
)

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("💼 HR Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

# ----------------------------
# Dashboard
# ----------------------------

if page == "Dashboard":

    st.title("💼 HR Assistant Dashboard")
    st.write("AI powered HR helpdesk for employees")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Employees", "120")
    col2.metric("HR Policies", "15")
    col3.metric("Announcements", "3")
    col4.metric("HR Queries Today", "27")

    st.markdown("---")

    st.subheader("📢 Latest HR Updates")

    st.write("• Annual appraisal cycle begins next month")
    st.write("• New work from home policy updated")
    st.write("• Health insurance benefits revised")

# ----------------------------
# HR Chatbot
# ----------------------------

elif page == "HR Chatbot":

    st.title("💬 HR Assistant Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display old messages
    for role, message in st.session_state.messages:

        if role == "user":
            st.chat_message("user").write(message)

        else:
            st.chat_message("assistant").write(message)

    # Chat input
    user_input = st.chat_input("Ask about HR policies...")

    if user_input:

        # Create vectorstore automatically if missing
        if not os.path.exists("vectorstore"):
            ingest_documents()

        qa_chain = get_qa_chain()

        st.chat_message("user").write(user_input)

        response = qa_chain.invoke({
            "query": str(user_input)
        })

        answer = response["result"]

        st.chat_message("assistant").write(answer)

        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("assistant", answer))

# ----------------------------
# Upload Documents
# ----------------------------

elif page == "Upload Documents":

    st.title("📄 Upload HR Documents")

    uploaded_file = st.file_uploader(
        "Upload HR Policy PDF",
        type=["pdf"]
    )

    if uploaded_file:

        os.makedirs("data", exist_ok=True)

        with open(f"data/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Document uploaded successfully")

# ----------------------------
# About
# ----------------------------

elif page == "About":

    st.title("ℹ️ About")

    st.write("""
    This HR Assistant is an AI-powered chatbot that answers
    employee questions using company HR policies.

    **Technology Stack**

    • Streamlit  
    • LangChain  
    • FAISS Vector Database  
    • HuggingFace Embeddings  
    • Groq LLM  
    """)