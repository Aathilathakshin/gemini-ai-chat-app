import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini Chat", page_icon="💬")
st.title("💬 Gemini AI Chat")

# API key from Streamlit Secrets
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("GEMINI_API_KEY secret set pannunga.")
    st.stop()

# Keep chat history during the session
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user's message
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                answer = response.text or "No response received."
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Error: {e}")
