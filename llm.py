import os
import google.generativeai as genai

API_KEY = os.getenv("GENAI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_disease_description(plant: str, disease: str) -> str:
    prompt = f"Write a short one paragraph explanation of {disease} disease on {plant}."
    response = model.generate_content(prompt)
    return response.text