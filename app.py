from ingest import ingest_documents
import streamlit as st
import os
import speech_recognition as sr
from src.qa_chain import get_qa_chain

st.set_page_config(
    page_title="HR Assistant",
    page_icon="🧳",
    layout="wide"
)

# --------------------------
# Authentication
# --------------------------

USERS = {
    "admin": "admin123",
    "employee1": "emp123",
    "employee2": "emp456"
}

def login():
    st.title("🔐 HR Assistant Login")
    st.write("Please login to continue")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# --------------------------
# Sidebar
# --------------------------

st.sidebar.title("🧳 HR Assistant")
st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.sidebar.divider()

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

    # --------------------------
    # Suggested Questions
    # --------------------------

    st.write("💡 **Suggested Questions:**")
    suggested = [
        "What is the leave policy?",
        "What are the working hours?",
        "How do I apply for work from home?",
        "What is the appraisal process?",
        "What are the health insurance benefits?"
    ]

    cols = st.columns(len(suggested))
    clicked_question = None
    for i, question in enumerate(suggested):
        with cols[i]:
            if st.button(question, use_container_width=True):
                clicked_question = question

    st.divider()

    # --------------------------
    # Voice Input
    # --------------------------

    st.write("🎤 **Voice Input:**")
    voice_col1, voice_col2 = st.columns([1, 5])
    voice_text = ""
    with voice_col1:
        if st.button("🎤 Speak"):
            with st.spinner("Listening..."):
                try:
                    recognizer = sr.Recognizer()
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, timeout=5)
                        voice_text = recognizer.recognize_google(audio)
                        st.session_state.voice_input = voice_text
                        st.success(f"You said: {voice_text}")
                except sr.WaitTimeoutError:
                    st.warning("No speech detected. Please try again.")
                except sr.UnknownValueError:
                    st.warning("Could not understand audio. Please try again.")
                except Exception as e:
                    st.error(f"Microphone error: {str(e)}")

    st.divider()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Determine input — voice, suggested button, or typed
    user_input = None
    if clicked_question:
        user_input = clicked_question
    elif "voice_input" in st.session_state and st.session_state.voice_input:
        user_input = st.session_state.voice_input
        st.session_state.voice_input = ""
    
    typed_input = st.chat_input("Ask about HR policies...")
    if typed_input:
        user_input = typed_input

    # Process the question
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    qa_chain = get_qa_chain()
                    response = qa_chain.invoke(str(user_input))
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

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
                st.success("✅ Document uploaded and processed successfully!")
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
    - SpeechRecognition (Voice Input)
    """)
