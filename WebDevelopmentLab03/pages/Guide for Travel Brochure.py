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
        tone = st.selectbox(
            "Choose Brochure Tone",
            [
                "Friendly Travel Guide",
                "Rick-style Warning",
                "Survival Guide",
                "Professional Brochure",
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
- Type: {loc_type}
- Dimension: {dimension}
- Number of known residents: {len(residents)}
- Sample Residents URLs: {resident_preview}

The brochure should be fun, immersive, and written as if the location
is a real tourist destination. It should:
- Describe the environment
- Explain cultural aspects
- Mention safety/danger levels
- Provide travel recommendations
- Make references to the show when relevant

Length: 2–4 paragraphs.
"""
    return prompt


def generate_brochure(prompt):
    response = model.generate_content(prompt)
    return response.text



with tab2:

    st.header("Your Generated Travel Brochure")

    if st.button("🚀 Generate Travel Brochure"):
        with st.spinner("Contacting the Galactic Federation..."):
            try:
                prompt = build_prompt(selected_location, tone)
                
                
                with st.expander("🔍 Show Prompt (Debug/Optional)"):
                    st.code(prompt)

                brochure_text = generate_brochure(prompt)

                st.subheader(f"🌎 Travel Brochure for {selected_location_name}")
                st.write(brochure_text)

            except Exception as e:
                st.error(f"Error generating brochure: {e}")
