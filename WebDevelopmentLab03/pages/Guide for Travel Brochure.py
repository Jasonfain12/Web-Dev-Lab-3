import streamlit as st
import requests
import google.generativeai as genai
import os


st.title("🪐 Interdimensional Travel Brochure Generator")


with st.container():
    key = st.secrets["key"]
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.success("Gemini AI ready!")


@st.cache_data
def fetch_locations():
    url = "https://rickandmortyapi.com/api/location"
    all_locations = []
    while url:
        res = requests.get(url)
        data = res.json()
        all_locations.extend(data["results"])
        url = data.get("info", {}).get("next")
    return all_locations

locations = fetch_locations()
location_names = [loc["name"] for loc in locations]


tab1, tab2 = st.tabs(["🌍 Select Settings", "📄 Generated Brochure"])



with tab1:

    st.header("Travel Brochure Settings")

    
    col1, col2 = st.columns(2)

    with col1:
        selected_location_name = st.selectbox(
            "Choose a Planet / Location:",
            location_names
        )

    with col2:

