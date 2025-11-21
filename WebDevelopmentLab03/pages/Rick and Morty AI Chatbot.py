import google.generativeai as genai
import os

print(genai.__file__)   # Where is this module loaded from?
print(genai.__version__)  # Confirm version again
print(hasattr(genai, "Client"))  # Is Client attribute present at all?
