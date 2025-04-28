from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

def clean_text(text):
    """Basic text cleaning."""
    import re
    text = text.encode('utf-8', errors='ignore').decode('utf-8')  # Remove weird unicode artifacts
    text = text.replace('\n', ' ').replace('\xa0', ' ')           # Replace newlines and non-breaking spaces
    text = re.sub(r'\s+', ' ', text)                              # Collapse multiple spaces
    text = text.strip()                                           # Strip leading/trailing whitespace
    return text

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        raw_text = ""
        for page in doc:
            raw_text += page.get_text()

        cleaned_text = clean_text(raw_text)

        return jsonify({
            "message": "File processed successfully.",
            "excerpt": cleaned_text[:500]  # Return first 500 cleaned characters
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend is live!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
