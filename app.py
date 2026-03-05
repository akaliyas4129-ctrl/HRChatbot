import streamlit as st
from src.qa_chain import get_qa_chain

# Page configuration
st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="wide"
)

# Title
st.title("💼 HR Assistant Dashboard")

# Sidebar
st.sidebar.title("💼 HR Assistant")
st.sidebar.caption("AI Powered HR Helpdesk")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

st.sidebar.divider()
st.sidebar.info("Built with Streamlit + LangChain")

# -------------------------
# Dashboard Page
# -------------------------
if page == "Dashboard":

    st.header("📊 HR Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍💼 Employees", "120")
    col2.metric("📄 Policies", "15")
    col3.metric("📢 Announcements", "3")
    col4.metric("💬 Queries Today", "27")

    st.divider()

    st.subheader("Recent HR Updates")

    st.write("• New remote work policy updated.")
    st.write("• Health insurance renewal starts next month.")
    st.write("• Annual leave reset on January 1.")

# -------------------------
# HR Chatbot Page
# -------------------------
elif page == "HR Chatbot":

    st.header("💬 Ask HR")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask a question about HR policies...")

    if user_input:
        qa_chain = get_qa_chain()
        response = qa_chain.run(user_input)

        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("assistant", response))

    for role, msg in st.session_state.messages:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

# -------------------------
# Upload Documents Page
# -------------------------
elif page == "Upload Documents":

    st.header("📄 Upload HR Documents")

    uploaded_file = st.file_uploader(
        "Upload HR policy documents",
        type=["pdf"]
    )

    if uploaded_file:
        st.success("Document uploaded successfully!")

# -------------------------
# About Page
# -------------------------
elif page == "About":

    st.header("ℹ️ About This App")

    st.write("""
    **HR Assistant Dashboard**

    This AI-powered HR chatbot helps employees quickly find answers about company policies.

    ### Features
    - 💬 HR policy chatbot
    - 📄 HR document search
    - 📊 HR dashboard overview
    - ⚡ Fast AI responses

    ### Tech Stack
    - Streamlit
    - LangChain
    - Groq LLM
    - FAISS Vector Database
    """)