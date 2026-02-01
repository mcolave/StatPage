import google.generativeai as genai
import sys

print(f"Python: {sys.version}")
print(f"GenAI: {genai.__version__}")
print(f"Dir: {dir(genai)}")

try:
    from google.generativeai import ImageGenerationModel
    print("Found: ImageGenerationModel")
except ImportError:
    print("Missing: ImageGenerationModel")
