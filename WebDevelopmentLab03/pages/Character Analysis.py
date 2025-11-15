import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import requests
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Character Info Page",
)

# PAGE TITLE AND INFORMATION
st.title("Rick and Morty Character Info Page!")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()

def getAllCharacters():
    #will form a list of dicitonaries containng info of every character
    #then, we will use pandas to organize it properly and determine amount of each species

    base_url = "https://rickandmortyapi.com/api/character?page="
    allCharacters = []
    for i in range (1, 43): #we know there are 43 total pages of characters in the API
        url = base_url + str(i) 
        response = requests.get(url)
        data = response.json()

        allCharacters += data["results"]

    return allCharacters

characters = getAllCharacters()
df = pd.DataFrame(characters)

#value_counts is a pandas function that will count how many of each value in each column of dataframe
speciesCounts = df["species"].value_counts()

st.title("Character Count by Species")
#.index returns row labels of dataframe (pandas)
species_options = list(speciesCounts.index)

selected_species = st.multiselect(

    "Select species to display:",
    options = species_options,
    default = ["Human"] #show only amount of characters that are humans at first
)

filtered_counts = speciesCounts[speciesCounts.index.isin(selected_species)]
st.bar_chart(filtered_counts)




st.divider()
st.title("Rick and Morty Character Viewer")

#species dropdown
species_options = sorted(df["species"].unique())
selected_species = st.selectbox("Select a species:", options=species_options)

#filter characters by selected species
filtered_df = df[df["species"] == selected_species]

#name dropdown (based on selected species)
name_options = sorted(filtered_df["name"].unique())
selected_name = st.selectbox("Select a character:", options=name_options)

#find character info
character = filtered_df[filtered_df["name"] == selected_name].iloc[0]

#display info
st.subheader(character["name"])
st.image(character["image"], width=250)

#display other info about character
st.write(f"**Status:** {character['status']}")
st.write(f"**Gender:** {character['gender']}")
st.write(f"**Origin:** {character['origin']['name']}")
st.write(f"**Location:** {character['location']['name']}")
st.write(f"**Species:** {character['species']}")
