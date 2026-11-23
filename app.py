 import streamlit as st
from google import genai

st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Gemini AI Chat")
st.caption("Chat with Google's Gemini AI")

# Create one reusable client
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


# Check whether the API key is available
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = get_client(api_key)
except Exception:
    st.error(
        "API key missing. Open Streamlit app settings → Secrets "
        "and add GEMINI_API_KEY."
    )
    st.stop()


# Keep chat history during the session
if "history" not in st.session_state:
    st.session_state.history = []


# Start a new chat
if st.button("🗑️ Clear chat"):
    st.session_state.history = []
    st.rerun()


# Display previous messages
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])


# Chat input
user_message = st.chat_input("Type your message...")

if user_message:
    # Display and save the user's message
    st.session_state.history.append(
        {"role": "user", "text": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # Prepare conversation history for Gemini
    contents = []

    for message in st.session_state.history:
        role = "user" if message["role"] == "user" else "model"
        contents.append(
            {
                "role": role,
                "parts": [{"text": message["text"]}]
            }
        )

    # Get Gemini's response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )

                assistant_message = response.text

                if not assistant_message:
                    assistant_message = "I couldn't generate a response. Please try again."

                st.markdown(assistant_message)

                st.session_state.history.append(
                    {"role": "assistant", "text": assistant_message}
                )

            except Exception as error:
                st.error(f"Request failed: {error}")
