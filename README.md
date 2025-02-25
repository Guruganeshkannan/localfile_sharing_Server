# localfile_sharing_Server

📂 FileShare - Local File Sharing System 🚀
FileShare is a simple and efficient local file-sharing system that allows users to upload and download files over a local network via a clean web UI. It supports drag-and-drop uploads, real-time progress tracking, and instant file downloads.

✨ Features
✅ Drag & Drop File Uploads – Simply drag files into the browser to upload.
✅ Upload Progress Bar – See real-time upload progress.
✅ Instant File Download – Click on a file to download it.
✅ No Page Reload – Uploads and updates happen dynamically.
✅ Minimalist & User-Friendly UI – Clean and easy to use.
✅ Runs on Local Network – No internet required.

🛠️ Installation & Setup
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/Guruganeshkannan/fileshare.git
cd fileshare
2️⃣ Install Dependencies
Ensure Python & Flask are installed:

sh
Copy
Edit
pip install flask
3️⃣ Run the Server
sh
Copy
Edit
python fileshare.py
4️⃣ Access the Web Interface
Open http://localhost:8080/ in your browser.
Drag & Drop files or click to upload.
Download files instantly from the displayed list.
🎨 Project Structure
bash
Copy
Edit
📂 fileshare/
│── 📂 templates/          # HTML UI files
│   ├── index.html        # Main web interface
│
│── 📂 uploads/            # Stored files (auto-created)
│── fileshare.py           # Flask backend
│── README.md              # Project documentation      
🔧 Technologies Used
Python 3
Flask (Micro Web Framework)
HTML, CSS, JavaScript
AJAX (for seamless uploads)
🚀 How It Works
Drag and drop files into the upload area.
Track real-time progress while the file uploads.
Files appear instantly in the download list.
Click on a file to download it to your device.
📌 Future Enhancements
🔹 Multi-user support
🔹 Password-protected downloads
🔹 Dark mode UI option
🔹 File preview before download

🤝 Contributing
Want to improve FileShare? Follow these steps:

Fork this repository.
Create a new branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add new feature").
Push to your fork (git push origin feature-name).
Submit a Pull Request 🚀
📝 License
This project is open-source and available under the MIT License.

📧 Contact
🔹 Author: Guruganesh
🔹 GitHub: guruganeshkannan16@gmail.com
🔹 Email: your.email@example.com

💡 FileShare makes local file sharing simple and efficient. Try it out today! 🚀📂
