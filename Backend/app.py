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
    language = data.get("language", "").strip()

    if not text or not language:
        return jsonify({"error": "Text and language must be provided."}), 400

    try:
        translated_text = translate_text(text, language)
        return jsonify({"translation": translated_text})
    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
