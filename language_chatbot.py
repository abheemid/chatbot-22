import streamlit as st
from google import genai
from google.genai import types

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Arti Chatbot",
    page_icon="💬",
    layout="centered"
)

# --------------------------------------------------
# Custom CSS (Design Only)
# --------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #f8f9fb 0%, #ffffff 100%);
}
.chat-title {
    font-size: 2rem;
    font-weight: 700;
}
.chat-subtitle {
    color: #6b7280;
    margin-bottom: 1rem;
}
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.8rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("<div class='chat-title'>💬 Arti Chatbot</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='chat-subtitle'>Chat with different AI personas using system instructions</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Gemini client
# --------------------------------------------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --------------------------------------------------
# Persona Definitions
# --------------------------------------------------
PERSONAS = {
    "Default Assistant": "You are a helpful, clear, and friendly assistant.",
    
    "Tamil Persona 🇮🇳": (
        "You are a friendly AI assistant who primarily responds in Tamil. "
        "Use simple, conversational Tamil with occasional English words if helpful. "
        "Be polite, warm, and culturally natural."
    ),
    
    "Telugu Persona 🇮🇳": (
        "You are a friendly AI assistant who primarily responds in Telugu. "
        "Use natural spoken Telugu, mixing light English where appropriate. "
        "Keep the tone respectful and approachable."
    ),
    
    "Marathi Persona 🇮🇳": (
        "You are a friendly AI assistant who primarily responds in Marathi. "
        "Use clear, conversational Marathi with a warm and helpful tone."
    ),
    
    "Hindi Persona 🇮🇳": (
        "You are a friendly AI assistant who primarily responds in Hindi. "
        "Use simple, conversational Hindi with optional Hinglish where natural. "
        "Keep responses polite and supportive."
    ),
}

# --------------------------------------------------
# Sidebar – Controls
# --------------------------------------------------
st.sidebar.title("⚙️ Settings")

st.sidebar.subheader("🧠 Persona")
selected_persona = st.sidebar.selectbox(
    "Choose Assistant Persona",
    options=list(PERSONAS.keys())
)

st.sidebar.subheader("✍️ System Prompt")
system_prompt = st.sidebar.text_area(
    "Customize System Instruction",
    value=PERSONAS[selected_persona],
    height=160,
    help="You can further edit the persona instructions here."
)

st.sidebar.subheader("🎨 Appearance")
assistant_name = st.sidebar.text_input("Assistant Name", value="Arti AI")

st.sidebar.info(
    "💡 Switching persona resets the chat.\n\n"
    "You can also manually tweak the system prompt for fine control."
)

# --------------------------------------------------
# Session State Initialization (CORE LOGIC UNCHANGED)
# --------------------------------------------------
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

# Reset chat if system prompt changes
if st.session_state.system_prompt != system_prompt:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )
    st.rerun()

# --------------------------------------------------
# Display Chat History
# --------------------------------------------------
for message in st.session_state.history:
    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "🤖"
    ):
        st.markdown(message["content"])

# --------------------------------------------------
# Chat Input
# --------------------------------------------------
if prompt := st.chat_input("Type your message here…"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.chat.send_message(prompt)
        reply = response.text
        st.markdown(f"**{assistant_name}:** {reply}")

    st.session_state.history.append({"role": "assistant", "content": reply})

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    "<div class='footer'>❤️ Made by <a href='https://www.linkedin.com/in/arati-bheemidi/' target='_blank'>Arti with AI</a></div>",
    unsafe_allow_html=True
)
