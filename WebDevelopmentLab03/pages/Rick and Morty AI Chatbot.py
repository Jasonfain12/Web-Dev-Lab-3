import streamlit as st
import requests
import google.generativeai as genai
import os

st.title("Rick and Morty Episode Expert Chatbot!")

key = st.secrets["key"]
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash")

# Let user select category and toggle raw API display
category = st.selectbox("Select API category", ["Character", "Location", "Episode"])
show_raw_api = st.checkbox("Show raw API response")

def fetch_api_data(category):
    base = "https://rickandmortyapi.com/api/"
    res = requests.get(base + category.lower())
    try:
        return res.json()
    except:
        return {"error": "API returned invalid response"}

api_data = fetch_api_data(category)

if show_raw_api:
    st.write(api_data)

# Initialize chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# User input
user_msg = st.chat_input("Ask the chatbot something!")

if user_msg:
    # Show user message
    with st.chat_message("user"):
        st.write(user_msg)
    st.session_state.chat_history.append(("user", user_msg))

    # Build conversation messages as plain text prompt (since generate_content expects prompt string)
    # We’ll combine system instructions and chat history into one prompt string.

    # Construct system prompt with API data
    system_prompt = (
        "You are a friendly, helpful chatbot specialized in using "
        "data from the Rick and Morty API to answer questions. "
        "Always respond clearly and accurately based on the data.\n\n"
        f"Here is the relevant API data for category '{category}': {api_data}\n\n"
        "Conversation history:\n"
    )

    # Add conversation history
    conversation_history_text = ""
    for role, text in st.session_state.chat_history:
        conversation_history_text += f"{role.capitalize()}: {text}\n"

    # Add current user message
    conversation_history_text += f"User: {user_msg}\nAssistant:"

    # Final prompt
    prompt = system_prompt + conversation_history_text

    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Sorry — Gemini encountered an error. Try asking again.\n\n{e}"

    # Show assistant message
    with st.chat_message("assistant", avatar="🤖"):
        st.write(bot_reply)

    st.session_state.chat_history.append(("assistant", bot_reply))
