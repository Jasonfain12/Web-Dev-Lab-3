import streamlit as st
import requests
from google import genai

st.title("Interdimensional Travel Brochure Generator")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("Gemini API key missing. Add it to Streamlit secrets.")

client = genai.Client(api_key=API_KEY)

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

st.header("Choose Your Destination")
selected_location_name = st.selectbox("Select a Planet / Location", location_names)

st.header("Choose Brochure Style")
tone = st.selectbox(
    "Travel Brochure Tone",
    ["Friendly Travel Guide", "Rick-style Sarcastic Warning", "Horror Survival Guide", "Professional Tourism Bureau"],
)

def get_location_data(name):
    for loc in locations:
        if loc["name"] == name:
            return loc
    return None

selected_location = get_location_data(selected_location_name)

if st.button("Generate Travel Brochure"):
    with st.spinner("Contacting the Galactic Federation... ✨"):
        dimension = selected_location.get("dimension", "Unknown Dimension")
        loc_type = selected_location.get("type", "Unknown Type")
        residents = selected_location.get("residents", [])

        resident_preview = residents[:5]

        prompt = f"""
        You are an AI travel brochure writer for the Rick and Morty universe.
        Create a travel brochure in the style of: {tone}.

        Location Details:
        - Name: {selected_location_name}
        - Type: {loc_type}
        - Dimension: {dimension}
        - Number of known residents: {len(residents)}
        - Sample Residents: {resident_preview}

        The brochure should be fun, immersive, and written as if the location
        is a real tourist destination. It should: 
        - Describe the environment
        - Explain cultural aspects
        - Mention safety/danger levels
        - Provide travel recommendations
        - Make references to the show when relevant

        Length: 2–4 paragraphs.
        """

        try:
            response = client.models.generate(
                model="gemini-1.5-flash",
                prompt=prompt,
            )
            st.subheader(f"📍 Travel Brochure for {selected_location_name}")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error generating brochure: {e}")
