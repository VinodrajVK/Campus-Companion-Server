import json
import difflib
import random
from datetime import datetime
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    filename='Campus_Companion.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load The JSON File
# Define the filename in a configuration section
INTENTS_JSON_FILE = "intents_with_variations.json"

# Load The JSON File
with open(INTENTS_JSON_FILE, "r") as file:
    intents_data = json.load(file)


# Predict The Intent


def get_intent(user_input):
    matches = difflib.get_close_matches(user_input.lower(), [
        pattern.lower() for intent in intents_data["intents"] for pattern in intent["patterns"]], n=3, cutoff=0.4)

    if matches:
        matched_intent = next(
            intent for intent in intents_data["intents"] if matches[0] in intent["patterns"])
        return matched_intent
    else:
        return None

# Generate The Response based on Intent


def get_response(intent):
    responses = intent["responses"]
    return random.choice(responses)

# Flask route for handling chatbot requests


@app.route('/chatbot', methods=['POST', 'GET'])
def chatbot():
    data = request.get_json()
    user_input = data.get('user_message', '')
    logger.info("User : %s", user_input)

    if user_input.lower() == 'exit':
        logger.info("User requested exit.")
        return jsonify({"response": "Goodbye!"})
    matched_intent = get_intent(user_input)

    if matched_intent:
        response = get_response(matched_intent)
        logger.info("Response : %s", response)
        return jsonify({"response": response})
    else:
        logger.warning("Unrecognized user input: %s", user_input)
        return jsonify({"response": "Sorry, I don't understand that. Can you please rephrase?"})


if __name__ == '__main__':
    logger.info("Bot: Hi! How can I assist you today?")
    app.run("0.0.0.0", port=5000, debug=True)
