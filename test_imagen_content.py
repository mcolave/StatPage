import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the model verified to exist
model_name = "models/imagen-4.0-fast-gen" 
print(f"Model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    print("Model initialized.")
    
    response = model.generate_content("A retro robot holding a sign")
    print("Response received.")
    print(f"Dir response: {dir(response)}")
    
    if response.parts:
        print(f"Parts count: {len(response.parts)}")
        print(f"Part 0 type: {type(response.parts[0])}")
        print(f"Part 0 dir: {dir(response.parts[0])}")
    else:
        print("No parts in response.")

except Exception as e:
    print(f"Error: {e}")
