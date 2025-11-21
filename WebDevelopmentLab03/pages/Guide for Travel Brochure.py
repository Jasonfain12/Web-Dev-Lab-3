import streamlit as st
import requests
import google.generativeai as genai

st.title("Interdimensional Travel Brochure Generator")

# Initialize the client with your API key from Streamlit secrets
key = st.secrets["key"]
client = genai.Client(api_key=key)

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

selected_location_name = st.selectbox("Select a Planet / Location", location_names)

tone = st.selectbox(
    "Choose Brochure Tone",
    [
        "Friendly Travel Guide",
        "Rick-style Sarcastic Warning",
        "Horror Survival Guide",
        "Professional Tourism Bureau",
    ],
)

def get_location_data(name):
    for loc in locations:
        if loc["name"] == name:
            return loc
    return None

selected_location = get_location_data(selected_location_name)

def build_prompt(location, tone):
    dimension = location.get("dimension", "Unknown Dimension")
    loc_type = location.get("type", "Unknown Type")
    residents = location.get("residents", [])
    resident_preview = residents[:5]

    prompt = f"""
You are an AI travel brochure writer for the Rick and Morty universe.
Create a travel brochure in the style of: {tone}.

Location Details:
- Name: {location['name']}
- Type:
