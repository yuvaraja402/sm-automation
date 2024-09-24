from flask import Flask, request, jsonify
import os, json

from requests_oauthlib import OAuth1Session
import vertexai
from vertexai.preview.generative_models import GenerativeModel

app = Flask(__name__)
#CORS(app)  # Enable CORS for all routes

'''
# Constants for file and API keys
TWITTER_API_URL = "https://api.twitter.com/2/tweets"



def create_tweet(tweet_text):
    # Load Twitter API credentials
    CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    # Check if any of the credentials are None
    if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        raise ValueError("Twitter API credentials are not properly set.")

    payload = {"text": tweet_text}

    # Create an OAuth1 session
    oauth = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_TOKEN_SECRET,
    )

    try:
        response = oauth.post(TWITTER_API_URL, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except Exception as err:
        print(f"An error occurred: {err}")
        return "Posting Failed"

    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

    return "Posting Success!"
'''
@app.route('/')
def homepage():
    return jsonify('Welcome to the App!')


def gemini_text_magic(input_text):
    project_id = "dynamic-return-426221-p1"
    location = "europe-west2"

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name="gemini-1.0-pro")
    chat = model.start_chat()

    prompt = f"""
    Here is my raw text before I post to social media - {input_text}
    Number of posts I want - 5, make each post look unique.
    Instructions per post:
    1- Make my entire text within 280 characters maximum limit.
    2- Add emojis and hashtags.
    3- Correct the entire text grammatically.
    4- Give output in this json format - "Post-number" : "<Text with emoji's> <br> <Hashtags>"
    """
    gemini_response = "" 
    try:
        response = chat.send_message(prompt)
        gemini_response = response.text
        return gemini_response
    except RuntimeError as e:
        print(f"Error from Vertex AI: {e}")
        return "Failed to beautify text."

# Function - /text will route the text here to get cleaned
#def clean_text(raw_text):
#    cleaned_text = raw_text.replace('**', '').replace('##', '')
#    return cleaned_text

# Frontend handler - user submits the text
@app.route('/beautifytext', methods=['POST'])
def beautifytext():
    raw_data = request.get_json()
    text_from_user = raw_data.get('user_text', '')
    gemini_response = gemini_text_magic(text_from_user)
    return jsonify({'message': gemini_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)