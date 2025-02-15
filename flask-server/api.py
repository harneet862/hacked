import google.generativeai as genai
import os
import sys

apiKey = "AIzaSyBvdonwgAsVyxSC90eW0w7PbBGfQZ84QAE"


# Configure API Key
genai.configure(api_key=apiKey)

# Function to generate a response from Gemini
def get_gemini_response(title, description):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Choose the model
    response = model.generate_content(
        f'just answer one word for this title: {title} and description: {description} '
        'classify it one of the category from the below: '
        'productivity, education, fitness, entertainment, socialmedia, blogging, news'
    )
    answer = response.candidates[0].content.parts[0].text.strip()
    return answer

