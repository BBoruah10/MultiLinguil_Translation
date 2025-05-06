from flask import Flask, request, jsonify
from flask_cors import CORS
from translate import translate_text
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body is missing or not in JSON format."}), 400

    text = data.get("text", "").strip()
    source_lang = data.get("source_lang", "").strip()
    target_lang = data.get("target_lang", "").strip()

    if not text or not source_lang or not target_lang:
        return jsonify({"error": "Text, source language, and target language must be provided."}), 400

    try:
        # Construct the language pair string (e.g., "English to Hindi")
        language_pair = f"{source_lang} to {target_lang}"
        
        # Translate text
        translated_text = translate_text(text, source_lang, target_lang)
        
        return jsonify({"translation": translated_text})
    
    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
