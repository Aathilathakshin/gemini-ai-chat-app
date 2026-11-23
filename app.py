import streamlit as st
from google import genai

st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="💬"
)

st.title("💬 Gemini AI Chat")
st.caption("Chat with Gemini AI")


# Get API key and create Gemini client
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error(
        "API key missing. Add GEMINI_API_KEY in "
        "Streamlit app settings → Secrets."
    )
    st.stop()


# Store chat history
if "history" not in st.session_state:
    st.session_state.history = []


# Clear chat button
if st.button("Clear chat"):
    st.session_state.history = []
    st.rerun()


# Display previous messages
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])


# Chat input
user_message = st.chat_input("Type your message...")


if user_message:
    # Save and display the user's message
    st.session_state.history.append(
        {"role": "user", "text": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # Convert chat history to Gemini format
    contents = []

    for message in st.session_state.history:
        if message["role"] == "user":
            role = "user"
        else:
            role = "model"

        contents.append(
            {
                "role": role,
                "parts": [{"text": message["text"]}]
            }
        )

    # Request Gemini response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Gemini is thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=contents
                )

            assistant_message = response.text

            if not assistant_message:
                st.warning("Gemini returned an empty response.")
            else:
                st.markdown(assistant_message)

                st.session_state.history.append(
                    {
                        "role": "assistant",
                        "text": assistant_message
                    }
                )

        except Exception as error:
            error_message = str(error)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                st.warning(
                    "Gemini server is busy right now. "
                    "Please wait a few minutes and try again."
                )
            else:
                st.error(f"Request failed: {error}")
