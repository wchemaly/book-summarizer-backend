from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

def basic_summarize(text):
    """
    Very simple summarizer:
    - Takes the first 2-3 paragraphs
    - Trims obvious junk
    - Prepares a clean, short blurb
    """
    # Basic cleanup
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())  # collapse multiple spaces

    # Try splitting into sentences
    sentences = text.split('. ')
    summary = '. '.join(sentences[:3])  # take first 3 sentences

    if not summary.endswith('.'):
        summary += '.'

    return summary.strip()

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        if not text.strip():
            return jsonify({"error": "Extracted text is empty"}), 400

        summary = basic_summarize(text)

        return jsonify({
            "message": "File processed successfully.",
            "summary": summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend is live and ready!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
