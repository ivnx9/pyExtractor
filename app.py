from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import textract

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Web Interface
@app.route("/", methods=["GET", "POST"])
def index():
    content = ""
    if request.method == "POST":
        f = request.files["file"]
        filename = secure_filename(f.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)

        content = extract_file_content(path, filename)
        os.remove(path)  # Delete after extraction

    return render_template("index.html", content=content)

# API Endpoint
@app.route("/extract", methods=["POST"])
def extract():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    filename = secure_filename(f.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(path)

    content = extract_file_content(path, filename)
    os.remove(path)  # Delete after extraction

    if content == "Unsupported file type.":
        return jsonify({"error": content}), 400

    return jsonify({"content": content})

# Core Extractor using textract
def extract_file_content(path, filename):
    try:
        if filename.endswith((".pdf", ".docx", ".pptx")):
            text = textract.process(path)
            return text.decode("utf-8", errors="ignore")
        else:
            return "Unsupported file type."
    except Exception as e:
        return f"Error extracting content: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
