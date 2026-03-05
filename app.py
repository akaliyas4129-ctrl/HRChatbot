import streamlit as st
import pandas as pd
from src.qa_chain import get_qa_chain

# Page configuration
st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="wide"
)

# Sidebar
st.sidebar.title("💼 HR Assistant")
st.sidebar.caption("AI Powered HR Helpdesk")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

st.sidebar.divider()
st.sidebar.info("Built with Streamlit + LangChain + Groq")

# Title
st.title("💼 HR Assistant Dashboard")
st.caption("AI powered HR helpdesk for employees")

st.divider()

# -----------------------
# DASHBOARD
# -----------------------

if page == "Dashboard":

    st.subheader("📊 Company Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍💼 Employees", "120")
    col2.metric("📄 HR Policies", "15")
    col3.metric("📢 Announcements", "3")
    col4.metric("💬 HR Queries Today", "27")

    st.divider()

    st.subheader("📈 HR Query Analytics")

    data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Queries": [12, 18, 10, 22, 27]
    })

    st.line_chart(data.set_index("Day"))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📢 Latest HR Updates")
        st.success("Remote work policy updated")
        st.info("Health insurance renewal next month")
        st.warning("Annual leave reset on January 1")

    with col2:
        st.subheader("⚡ Quick Actions")
        st.button("💬 Ask HR Chatbot")
        st.button("📄 Upload HR Policy")

# -----------------------
# HR CHATBOT
# -----------------------

elif page == "HR Chatbot":

    st.subheader("💬 HR Assistant Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask about HR policies...")

    if user_input:

        qa_chain = get_qa_chain()

        response = qa_chain.invoke({"query": str(user_input)})
        answer = response["result"]

        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("assistant", answer))

    for role, msg in st.session_state.messages:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

# -----------------------
# UPLOAD DOCUMENTS
# -----------------------

elif page == "Upload Documents":

    st.subheader("📄 Upload HR Documents")

    uploaded_file = st.file_uploader(
        "Upload HR Policy PDFs",
        type=["pdf"]
    )

    if uploaded_file:
        st.success("Document uploaded successfully!")

# -----------------------
# ABOUT PAGE
# -----------------------

elif page == "About":

    st.subheader("ℹ️ About This Application")

    st.write("""
This **AI-powered HR Assistant** helps employees quickly find answers about company policies.

### Features
- 💬 HR Chatbot
- 📄 Document Search
- 📊 HR Dashboard
- ⚡ Fast AI responses

### Technology
- Streamlit
- LangChain
- Groq LLM
- FAISS Vector Database
""")