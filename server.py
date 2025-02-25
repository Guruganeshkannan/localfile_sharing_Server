from flask import Flask, render_template, request, send_from_directory, jsonify
import os

app = Flask(__name__)

# Define Upload Folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home Route - Show File List
@app.route("/")
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)

# Upload Route (Handles Asynchronous Upload)
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded", "status": "error"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected", "status": "error"})

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully!", "status": "success"})

# Download Route
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
