from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Read PDF and extract text
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        return jsonify({
            "message": "File processed successfully.",
            "excerpt": text[:500]  # Just first 500 characters for now
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