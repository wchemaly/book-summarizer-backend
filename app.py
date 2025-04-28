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
 @@ -25,24 +36,27 @@
 
     try:
         doc = fitz.open(stream=file.read(), filetype="pdf")
         raw_text = ""
         text = ""
         for page in doc:
             raw_text += page.get_text()
             text += page.get_text()
 
         cleaned_text = clean_text(raw_text)
         if not text.strip():
             return jsonify({"error": "Extracted text is empty"}), 400
 
         summary = basic_summarize(text)
 
         return jsonify({
             "message": "File processed successfully.",
             "excerpt": cleaned_text[:500]  # Return first 500 cleaned characters
             "summary": summary
         })
     except Exception as e:
         return jsonify({"error": str(e)}), 500
 
 @app.route("/")
 def home():
     return "Backend is live!"
     return "Backend is live and ready!"
 
 if __name__ == "__main__":
     import os
     port = int(os.environ.get("PORT", 5000))
     app.run(host="0.0.0.0", port=port)
