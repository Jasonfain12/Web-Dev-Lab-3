import google.generativeai as genai
import os

st.write(genai.__file__)   # Where is this module loaded from?
st.write(genai.__version__)  # Confirm version again
st.write(hasattr(genai, "Client"))  # Is Client attribute present at all?
