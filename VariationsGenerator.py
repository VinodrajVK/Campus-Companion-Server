import json
import random
from nltk.tokenize import word_tokenize


def generate_sentence_variations(sentence, num_variations=8):
    variations = []

    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    for _ in range(num_variations):
        # Shuffle the words to create a variation
        random.shuffle(words)
        new_variation = ' '.join(words)
        variations.append(new_variation)

    return variations


def generate_variations_for_intents(intents_data, num_variations=3):
    new_intents_data = {"intents": []}

    for intent in intents_data["intents"]:
        new_patterns = []

        for pattern in intent["patterns"]:
            variations = generate_sentence_variations(pattern, num_variations)
            new_patterns.extend(variations)

        # Include the original patterns along with their variations
        new_patterns.extend(intent["patterns"])

        # Remove duplicates
        new_patterns = list(set(new_patterns))
        if 'responses' in intent:
            new_intent = {
                "tag": intent["tag"],
                "patterns": new_patterns,
                "responses": intent["responses"]
            }

        new_intents_data["intents"].append(new_intent)

    return new_intents_data


# Load intents from the original file
with open("intents.json", "r") as file:
    original_intents_data = json.load(file)

# Generate variations for each sentence in the patterns
new_intents_data = generate_variations_for_intents(
    original_intents_data, num_variations=5)

# Save the new intents data to a new file
with open("intents_with_variations.json", "w") as file:
    json.dump(new_intents_data, file, indent=2)

print("Variations Generated and saved to intents_with_variations.json.")
