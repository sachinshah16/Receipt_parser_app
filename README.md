
# 🧾 Receipt Parser App

A simple web application built with **Flask** that extracts key information (vendor, amount, date) from uploaded receipts (images or PDFs) using **Tesseract OCR** and stores the results in a **SQLite** database. Users can view, edit, and analyze uploaded receipt data through a web interface.

---

## 🔧 Features

- 📤 Upload receipts in `.jpg`, `.png`, or `.pdf` formats
- 🤖 Automatically extract:
  - Vendor name
  - Total amount
  - Date of purchase
- ✅ Confirm and edit extracted data before saving
- 🗂 View, search, sort, and filter receipts
- ✏️ Edit or delete saved receipts
- 📊 Dashboard with basic analytics (monthly spend, top vendors, etc.)

---

## 🖥️ Tech Stack

- Python 3.x
- Flask
- Tesseract OCR
- SQLite (via SQLAlchemy)
- Jinja2 Templates
- HTML + CSS

---

## 📸 Screenshots

### 1. Upload Page
![Upload Receipt](screenshots/upload.png)

### 2. Receipt Confirmation Page
![Confirm Data](screenshots/confirm_data.png)

### 3. Receipt Dashboard
![Dashboard](screenshots/dashboard.png)

### 3. Edit Receipt
![Dashboard](screenshots/edit.png)

### 3. Veiw Receipts
![Dashboard](screenshots/receipts.png)

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/receipt-parser-app.git
cd receipt-parser-app
```

### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

- **Windows:** [Download here](https://github.com/tesseract-ocr/tesseract/wiki)
- **Linux (Ubuntu):**
  ```bash
  sudo apt install tesseract-ocr
  ```
- **macOS:**
  ```bash
  brew install tesseract
  ```

> Make sure to update the path to the Tesseract executable in `parser.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## 🏃 Running the App

```bash
python app.py
```

Go to `http://127.0.0.1:5000/` in your browser.

---

## 📁 Folder Structure

```
receipt-parser-app/
│
├── app.py                # Flask app
├── parser.py             # OCR and data extraction logic
├── models.py             # SQLAlchemy ORM models
├── db.py                 # DB engine and session setup
├── templates/            # Jinja2 HTML templates
├── uploads/              # Uploaded images and PDFs
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🧠 Future Enhancements

- Advanced NLP for more accurate parsing
- Use Document AI or Cloud Vision APIs (optional)
- Export data to Excel or CSV
- User authentication (for multi-user support)

---

## 📃 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Made with ❤️ by **Sachin Kumar Shah**

- [LinkedIn](https://linkedin.com/in/sachin-shah16)
- [GitHub](https://github.com/sachinshah16)
