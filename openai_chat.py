import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(page_title="OpenAI Chatbot", page_icon="💬")

# Header
st.title("💬 OpenAI Chatbot")
st.caption("A simple chatbot powered by OpenAI's GPT model")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from OpenAI
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Sidebar
st.sidebar.title("About")
st.sidebar.info("This chatbot uses OpenAI's GPT-4o-mini model to have conversations with you.")
st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by [Build Fast with AI](https://buildfastwithai.com)")
