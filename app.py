import streamlit as st
from src.qa_chain import get_qa_chain

st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 HR Assistant Dashboard")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

# Dashboard
if page == "Dashboard":
    st.header("📊 HR Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Employees", "120")
    col2.metric("Open Positions", "8")
    col3.metric("Policies Available", "15")

    st.info("Use the sidebar to navigate through the HR Assistant.")

# Chatbot
elif page == "HR Chatbot":
    st.header("💬 Ask HR")

    query = st.text_input("Ask a question about HR policies")

    if query:
        qa_chain = get_qa_chain()
        response = qa_chain.run(query)
        st.success(response)

# Upload
elif page == "Upload Documents":
    st.header("📄 Upload HR Documents")

    uploaded_file = st.file_uploader("Upload HR policy PDF", type=["pdf"])

    if uploaded_file:
        st.success("File uploaded successfully!")

# About
elif page == "About":
    st.header("ℹ️ About This App")

    st.write("""
    This HR Assistant helps employees find answers about company policies using AI.
    
    Features:
    - HR policy chatbot
    - Document search
    - HR analytics dashboard
    """)