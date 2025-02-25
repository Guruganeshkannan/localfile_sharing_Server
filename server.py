from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for
import os
from datetime import datetime
from io import BytesIO
import socket
import pyqrcode  # Ensure you install this via: pip install pyqrcode

app = Flask(__name__)

# Define Upload Folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Get the server's IPv4 address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a public DNS server; the IP isn't actually used
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Print an ASCII QR code in the terminal using pyqrcode
def print_qr_terminal(data):
    qr = pyqrcode.create(data)
    # Print with a quiet zone of 1
    print(qr.terminal(quiet_zone=1))

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
        return jsonify({"message": "No file uploaded 😕", "status": "error"})
    
    files = request.files.getlist("file")
    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        saved_files.append(file.filename)
    if saved_files:
        return jsonify({"message": "Files uploaded successfully! 🎉", "status": "success"})
    else:
        return jsonify({"message": "No valid files uploaded 😕", "status": "error"})

# Single File Download Route
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Preview Route - Displays images or text file contents
@app.route("/preview/<filename>")
def preview(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        return "File not found 😢", 404
    
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.gif']:
        return f'''
        <html>
            <head><title>Preview: {filename} 📸</title></head>
            <body style="text-align:center; padding:20px;">
                <h2>Preview: {filename} 📸</h2>
                <img src="/download/{filename}" style="max-width:100%; border:5px solid #ff6f61; border-radius:10px;" />
            </body>
        </html>
        '''
    elif ext in ['.txt', '.py', '.html', '.css', '.js']:
        try:
            with open(file_path, 'r', encoding="utf8") as f:
                content = f.read()
            import html
            content = html.escape(content)
            return f'''
            <html>
                <head><title>Preview: {filename} 📄</title></head>
                <body style="text-align:left; padding:20px;">
                    <h2>Preview: {filename} 📄</h2>
                    <pre style="background:#f4f4f4; padding:10px; border-radius:5px;">{content}</pre>
                </body>
            </html>
            '''
        except Exception as e:
            return f"Error reading file: {str(e)} 😢", 500
    else:
        return "Preview not available for this file type 😕"

# Delete Route - Deletes a specified file
@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"Deleted {filename} 🗑️", "status": "success"})
    else:
        return jsonify({"message": "File not found 😕", "status": "error"})

# QR Code image route using an external API (redirects to a QR code generator)
@app.route("/qr_img")
def qr_img():
    ip = get_ip()
    url = f"http://{ip}:8080"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?data={url}&size=200x200"
    return redirect(qr_url)

if __name__ == "__main__":
    ip = get_ip()
    url = f"http://{ip}:8080"
    print("Server URL:", url)
    print_qr_terminal(url)
    app.run(host="0.0.0.0", port=8080, debug=True)
