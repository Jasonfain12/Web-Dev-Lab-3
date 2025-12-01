import streamlit as st
import requests
import google.generativeai as genai
import os

st.title("Rick and Morty Episode Expert Chatbot!")

key = st.secrets["key"]
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash")

st.write("Choose a category to chat about!")
category = st.selectbox("Select API category", ["Character", "Location", "Episode"])

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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

user_msg = st.chat_input("Ask the chatbot something!")

if user_msg:
    with st.chat_message("user"):
        st.write(user_msg)
    st.session_state.chat_history.append(("user", user_msg))

    system_prompt = (
        "You are a friendly, helpful chatbot specialized in using "
        "data from the Rick and Morty API to answer questions. "
        "Always respond clearly and accurately based on the data.\n\n"
        f"Here is the relevant API data for category '{category}': {api_data}\n\n"
        "Conversation history:\n"
    )

    conversation_history_text = ""
    for role, text in st.session_state.chat_history:
        conversation_history_text += f"{role.capitalize()}: {text}\n"

    conversation_history_text += f"User: {user_msg}\nAssistant:"

    prompt = system_prompt + conversation_history_text

    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Sorry — Gemini encountered an error. Try asking again.\n\n{e}"

    with st.chat_message("assistant", avatar="🤖"):
        st.write(bot_reply)

    st.session_state.chat_history.append(("assistant", bot_reply))
