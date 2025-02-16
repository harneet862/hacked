import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("API_KEY")


# Configure API Key
genai.configure(api_key=apiKey)

# Function to generate a response from Gemini
def get_gemini_response_category(title, description):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Choose the model
    response = model.generate_content(
        f'just answer one word for this title: {title} and description: {description} '
        'classify it one of the category from the below: '
        'productivity, education, fitness, entertainment, socialmedia, blogging, news'
    )
    answer = response.candidates[0].content.parts[0].text.strip()
    return answer

def get_gemini_response_bool(url, des, event_title):
    model = genai.GenerativeModel("gemini-1.5-flask")
    response = model.generate_content(
        f'give me answer in one word if url= {url} and desciption={des} is loosely related with event_title= {event_title}'
    )
    answer =  response.candidates[0].content.parts[0].text.strip()
    return answer