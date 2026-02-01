import google.generativeai as genai
import os

path = os.path.dirname(genai.__file__)
with open("genai_dir.txt", "w") as f:
    f.write(path)
print(f"Saved: {path}")
