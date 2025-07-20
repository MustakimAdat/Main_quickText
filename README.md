# 🚀 QuickText

QuickText is a lightweight web application that allows users to instantly share text and files across devices. It's designed to be fast, minimal, and easy to use — like an instant clipboard with optional file sharing support.

---

## 📌 Features

- ✅ Share text instantly between devices
- ✅ Upload and share files (max size: **200 MB**)
- ✅ Clean, responsive UI with **Tailwind CSS**
- ✅ Python backend with **MySQL** database
- ✅ No authentication required (for simple sharing)
- ✅ Works on desktop and mobile

---

## 🧑‍💻 Tech Stack

| Part         | Technology           |
|--------------|----------------------|
| Frontend     | HTML, CSS, Tailwind CSS |
| Backend      | Python (Flask or similar) |
| Database     | MySQL                |
| File Upload  | HTML5 + Python logic |
| Deployment   | *Your choice* (e.g., PythonAnywhere, Render, etc.)

---

## 🚧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quicktext.git
cd quicktext

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Configure database (MySQL)
Create a MySQL database (e.g., quicktext)

Update database credentials in your config.py or .env file (if used)

Run the app

```
python app.py
```

