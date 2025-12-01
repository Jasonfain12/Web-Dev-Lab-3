import streamlit as st
import pandas as pd
import json
import requests


st.set_page_config(
    page_title="Character Info Page",
)


st.title("Rick and Morty Character Info Page!")

st.divider()

with st.container():

    def getAllCharacters():
        base_url = "https://rickandmortyapi.com/api/character?page="
        allCharacters = []
        for i in range(1, 43):  # 43 total pages
            url = base_url + str(i)
            response = requests.get(url)
            data = response.json()
            allCharacters += data["results"]
        return allCharacters

    characters = getAllCharacters()
    df = pd.DataFrame(characters)

st.success("Character data loaded successfully!")


tab1, tab2 = st.tabs(["📊 Species Statistics", "🧪 Character Viewer"])


with tab1:

    st.header("Character Count by Species")

    speciesCounts = df["species"].value_counts()
    species_options = list(speciesCounts.index)

    selected_species = st.multiselect(
        "Select species to display:",
        options=species_options,
        default=["Human"]
    )

    filtered_counts = speciesCounts[speciesCounts.index.isin(selected_species)]

    st.subheader("Species Distribution")
    st.bar_chart(filtered_counts)



with tab2:

    st.header("Rick and Morty Character Viewer")

    # Species dropdown
    species_options = sorted(df["species"].unique())
    selected_species = st.selectbox("Select a species:", options=species_options)

    # Filter characters
    filtered_df = df[df["species"] == selected_species]

    # Name dropdown
    name_options = sorted(filtered_df["name"].unique())
    selected_name = st.selectbox("Select a character:", options=name_options)

    # Fetch the character
    character = filtered_df[filtered_df["name"] == selected_name].iloc[0]

    # Split the character section into 2 columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(character["image"], width=250)

    with col2:
        st.subheader(character["name"])
        st.write(f"**Status:** {character['status']}")
        st.write(f"**Gender:** {character['gender']}")
        st.write(f"**Origin:** {character['origin']['name']}")
        st.write(f"**Location:** {character['location']['name']}")
        st.write(f"**Species:** {character['species']}")

