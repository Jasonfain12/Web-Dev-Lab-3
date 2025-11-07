import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.
import matplotlib.pyplot as plt
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Character Analyzation",
    page_icon="👨",
)

# PAGE TITLE AND INFORMATION
st.title("Rick and Morty Character Profiles")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
