from google import genai
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gc_client = genai.Client(api_key=GOOGLE_API_KEY)

