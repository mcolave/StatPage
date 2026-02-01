import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit()

genai.configure(api_key=api_key)

print(f"Checking API Key: {api_key[:5]}...{api_key[-4:]}")

try:
    # Try to list models and find imagen
    print("Listing available models...")
    found_imagen = False
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
             # Just printing text models for debug, but we look for image capability
             pass
        if "image" in m.name.lower():
             print(f"Found Image Model: {m.name}")
             print(f"Supported Methods: {m.supported_generation_methods}")
             found_imagen = True
    
    if not found_imagen:
        print("Compatible Imagen model not explicitly listed (might still work via direct call).")

    # Try a generation
    print("\nAttempting to generate a test image...")
    # Note: proper SDK method for imagen might vary, assuming standard model fallback or failure
    # Currently standard free tier often doesn't grant image gen access, but let's try.
    
    # This is a hypothetical call as the SDK evolves.
    # If this fails, it often means the key doesn't have access.
    try:
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        response = model.generate_content("A cute robot holding a sign that says Hello")
        # Imagen usually returns a different structure, but if we get here without auth error, it's promising.
        print("Strict generation check: Attempted call.")
        print(f"Response type: {type(response)}")
    except Exception as e:
        print(f"Direct generation failed: {e}")

except Exception as e:
    print(f"Error during check: {e}")
