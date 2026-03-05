import streamlit as st
import pandas as pd
from src.qa_chain import get_qa_chain

st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

body {
    background-color:#F4F6FB;
}

.metric-card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
}

.metric-number {
    font-size:32px;
    font-weight:700;
}

.metric-title {
    font-size:16px;
}

.hero {
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    padding:30px;
    border-radius:15px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("💼 HR Assistant")
st.sidebar.caption("AI Powered HR Helpdesk")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "HR Chatbot", "Upload Documents", "About"]
)

st.sidebar.divider()
st.sidebar.info("Built with Streamlit + LangChain + Groq")

# ---------- HERO SECTION ----------
st.markdown("""
<div class="hero">
<h1>💼 HR Assistant Dashboard</h1>
<p>AI powered HR helpdesk for employees</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- DASHBOARD ----------
if page == "Dashboard":

    st.subheader("📊 Company Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Employees</div>
        <div class="metric-number">120</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">HR Policies</div>
        <div class="metric-number">15</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Announcements</div>
        <div class="metric-number">3</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Queries Today</div>
        <div class="metric-number">27</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("📈 HR Query Analytics")

    data = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri"],
        "Queries": [12,18,10,22,27]
    })

    st.line_chart(data.set_index("Day"))

    st.write("")

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

# ---------- CHATBOT ----------
elif page == "HR Chatbot":

    st.subheader("💬 HR Assistant Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask about HR policies...")

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
This **AI-powered HR Assistant** helps employees quickly find answers about HR policies.

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