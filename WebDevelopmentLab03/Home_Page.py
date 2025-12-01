import streamlit as st


with st.container():
    st.title("Web Development Lab03")


with st.container():
    st.header("CS 1301")
    st.subheader("Team 37, Web Development - Section E")

    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Daniel Galante")
    with col2:
        st.subheader("Jason Fain")


with st.container():
    st.header("Welcome!")

    st.write("""
Welcome to our Streamlit Web Development Lab03 app!  
Use the **sidebar** on the left to navigate through the pages.
""")


st.header("App Pages Overview")

tab1, tab2, tab3 = st.tabs(["Character Analysis", "Travel Brochure", "AI Chatbot"])

with tab1:
    st.write("""
### **Character Analysis**
Explore detailed information and visual analytics for all characters in the Rick and Morty universe.  
Includes:
- API data exploration  
- Graphs & charts  
- Character insights  
    """)

with tab2:
    st.write("""
### **Guide for Travel Brochure**
Generate a fully customized travel brochure for *any* planet or dimension.  
Features:
- Tone selection (Friendly, Survival Guide, Rick-Style Warning, etc.)  
- Real Rick and Morty API location data  
- AI-generated multi-paragraph brochure  
    """)

with tab3:
    st.write("""
### **Rick and Morty AI ChatBot**
Chat with an AI that specializes in:
- Episodes  
- Locations  
- Characters    
Uses the Rick and Morty API + Gemini to answer your questions.  
    """)




