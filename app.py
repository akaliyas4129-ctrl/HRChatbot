import streamlit as st
from src.qa_chain import get_qa_chain

st.set_page_config(
    page_title="HR Onboarding Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Employee Onboarding Assistant")
st.markdown("Ask questions about company HR policies.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("Ask about company policies..."):
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching HR documents..."):
            chain = get_qa_chain()
            answer = chain.invoke(question)
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})