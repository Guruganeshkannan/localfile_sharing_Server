from flask import Flask, render_template, request, send_from_directory, jsonify, send_file, redirect, url_for
import os
from datetime import datetime
from io import BytesIO
import zipfile

app = Flask(__name__)

# Define Upload Folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Template filter to format timestamps
@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

# Home Route - List files with upload times
@app.route("/")
def home():
    file_list = []
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        upload_time = os.path.getmtime(file_path)
        file_list.append({"name": filename, "upload_time": upload_time})
    file_list.sort(key=lambda x: x["upload_time"], reverse=True)
    return render_template("index.html", files=file_list)

# Upload Route (Handles Multiple File Uploads)
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded", "status": "error"})
    
    files = request.files.getlist("file")
    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        saved_files.append(file.filename)
    if saved_files:
        return jsonify({"message": "Files uploaded successfully!", "status": "success"})
    else:
        return jsonify({"message": "No valid files uploaded", "status": "error"})

# Single File Download Route
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Batch Download Route - Creates a ZIP archive of selected files
@app.route("/batch_download", methods=["POST"])
def batch_download():
    files = request.form.getlist("files")
    if not files:
        return redirect(url_for('home'))
    
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in files:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=file)
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename="files.zip", as_attachment=True)

# Preview Route - Displays images or text file contents
@app.route("/preview/<filename>")
def preview(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.gif']:
        # Display image in a simple HTML
        return f'<html><body><h2>Preview: {filename}</h2><img src="/download/{filename}" style="max-width:100%;"/></body></html>'
    elif ext in ['.txt', '.py', '.html', '.css', '.js']:
        try:
            with open(file_path, 'r', encoding="utf8") as f:
                content = f.read()
            import html
            content = html.escape(content)
            return f'<html><body><h2>Preview: {filename}</h2><pre>{content}</pre></body></html>'
        except Exception as e:
            return f"Error reading file: {str(e)}", 500
    else:
        return "Preview not available for this file type."

# Delete Route - Deletes a specified file
@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"Deleted {filename}", "status": "success"})
    else:
        return jsonify({"message": "File not found", "status": "error"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
