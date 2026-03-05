import streamlit as st
from src.qa_chain import get_qa_chain

# Page config
st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>

.main-title {
font-size:42px;
font-weight:700;
color:#2C3E50;
}

.subtitle {
font-size:18px;
color:gray;
}

.card {
background-color:#f9fafc;
padding:20px;
border-radius:12px;
box-shadow:0px 4px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("💼 HR Assistant")
st.sidebar.caption("AI Powered HR Helpdesk")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

st.sidebar.divider()
st.sidebar.info("Built using Streamlit + LangChain + Groq")

# ---------- HEADER ----------
st.markdown('<p class="main-title">HR Assistant Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI powered HR helpdesk for employees</p>', unsafe_allow_html=True)

st.divider()

# ---------- DASHBOARD ----------
if page == "Dashboard":

    st.subheader("📊 Company Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👨‍💼 Employees", "120")

    with col2:
        st.metric("📄 HR Policies", "15")

    with col3:
        st.metric("📢 Announcements", "3")

    with col4:
        st.metric("💬 HR Queries Today", "27")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📢 Latest HR Updates")
        st.write("• Remote work policy updated")
        st.write("• Health insurance renewal next month")
        st.write("• Annual leave reset on January 1")

    with col2:
        st.markdown("### 🧑‍💼 HR Support")
        st.info("Use the HR Chatbot to quickly find answers about HR policies, benefits, and employee guidelines.")

# ---------- CHATBOT ----------
elif page == "HR Chatbot":

    st.subheader("💬 HR Assistant Chat")

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

# ---------- DOCUMENT UPLOAD ----------
elif page == "Upload Documents":

    st.subheader("📄 Upload HR Documents")

    uploaded_file = st.file_uploader(
        "Upload HR Policy PDFs",
        type=["pdf"]
    )

    if uploaded_file:
        st.success("Document uploaded successfully!")

# ---------- ABOUT ----------
elif page == "About":

    st.subheader("ℹ️ About This Application")

    st.write("""
This **AI-powered HR Assistant** helps employees quickly find answers about company policies.

### Key Features

- 💬 AI HR Chatbot
- 📄 HR Document Search
- 📊 HR Dashboard
- ⚡ Fast responses powered by Groq

### Tech Stack

- Streamlit
- LangChain
- Groq LLM
- FAISS Vector Database
""")