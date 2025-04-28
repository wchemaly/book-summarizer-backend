from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF

# Initialize Flask app
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
        # Read and extract text from the uploaded PDF file
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        # Return a short excerpt to verify
        return jsonify({
            "message": "File processed successfully.",
            "excerpt": text[:500]  # First 500 characters
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ Backend is live and running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
