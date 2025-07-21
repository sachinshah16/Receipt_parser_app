import pytesseract
from PIL import Image
import re
from pdf2image import convert_from_path
import os

# Set Tesseract path (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_file(filepath):
    if filepath.lower().endswith('.pdf'):
        images = convert_from_path(filepath)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text
    else:
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)


def extract_receipt_data(filepath):
    text = extract_text_from_file(filepath)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    flat_text = " ".join(lines).lower()

    # --- Vendor Detection ---
    vendor = "Unknown"
    for line in lines[:5]:
        if line.isupper() and "INVOICE" not in line and len(line) > 3:
            vendor = line.title()
            break
    if vendor == "Unknown" and lines:
        vendor = lines[0].title()

    # --- Amount Extraction ---
    amount = None
    i = len(lines) - 1

    while i >= 0:
        line = lines[i].lower()
        if any(keyword in line for keyword in ["net to pay", "total", "grand total", "amount"]):
            # Try current line
            found = re.findall(r"\d{1,5}[.,]?\d{0,2}", lines[i])
            if not found and i + 1 < len(lines):
                # Try next line
                found = re.findall(r"\d{1,5}[.,]?\d{0,2}", lines[i + 1])

            if found:
                try:
                    amount_str = found[-1].replace(',', '').replace(' ', '')
                    amount = float(amount_str)
                    break
                except ValueError:
                    pass
        i -= 1

    if amount is None:
        # Fallback: find highest reasonable value
        found = re.findall(r"(?<!\d)(\d{1,5}(?:,\d{3})*(?:\.\d{2})?)(?!\d)", flat_text)
        if found:
            try:
                numeric_values = [float(f.replace(',', '')) for f in found]
                amount = max(numeric_values)
            except ValueError:
                amount = None

    # --- Date Extraction ---
    date = None
    date_patterns = [
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2}-\d{2}-\d{4}',
        r'\d{4}-\d{2}-\d{2}',
        r'[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}',
        r'\d{2}/\d{2}/\d{2}',
        r'\d{2}\s*[-]\s*[A-Za-z]{3,}\s*[-]\s*\d{4}',
    ]
    for pattern in date_patterns:
        for line in lines:
            match = re.search(pattern, line)
            if match:
                date = match.group()
                break
        if date:
            break

    return {
        'vendor': vendor,
        'amount': amount,
        'date': date
    }


# Example use:
# filepath = r"N:\Coding\Reciept_app\uploads\Apoorva.jpeg"
# print(extract_text_from_file(filepath))
