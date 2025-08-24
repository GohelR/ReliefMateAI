import streamlit as st
import google.generativeai as genai

# Load Gemini API key from secrets
api_key = st.secrets["general"]["GEMINI_API_KEY"]

# Configure Gemini
genai.configure(api_key=api_key)

# Create model instance
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini AI Chatbot")
st.write("Chat with Google's Gemini inside Streamlit!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error: {e}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
