import streamlit as st
import requests
import google.generativeai as genai

st.title("Rick and Morty Episode Expert Chatbot!")

genai.configure(api_key = st.secrets["key"])
client = genai.Client()


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

# Display Chat History

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# Chat Input
user_msg = st.chat_input("Ask the chatbot something!")

if user_msg:

    # Display user's message
    with st.chat_message("user"):
        st.write(user_msg)
    st.session_state.chat_history.append(("user", user_msg))

    # Build LLM Messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly, helpful chatbot specialized in using "
                "data from the Rick and Morty API to answer questions. "
                "Always respond clearly and accurately based on the data."
            )
        },
        {
            "role": "system",
            "content": f"Here is the relevant API data for category '{category}': {api_data}"
        }
    ]

    # Add conversation history
    for role, text in st.session_state.chat_history:
        messages.append({"role": role, "content": text})

    # Gemini Response with Try/Except
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=messages
        )
        bot_reply = response.text
    except Exception:
        bot_reply = "Sorry — Gemini encountered an error. Try asking again."

    # Display bot response
    with st.chat_message("assistant", avatar="🤖"):
        st.write(bot_reply)

    st.session_state.chat_history.append(("assistant", bot_reply))
