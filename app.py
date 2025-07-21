# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for,send_from_directory
import os
from parser import extract_receipt_data
from db import db_session, Receipt, Base, engine

from models import Receipt, Base
from werkzeug.utils import secure_filename
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Create the table when app starts
Base.metadata.create_all(engine)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract receipt data using Tesseract
        extracted_data = extract_receipt_data(filepath)

        # Show editable form with extracted data
        return render_template('confirm_data.html', receipt=extracted_data, filename=filename)

    # If GET request, show upload form
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def index():
    return render_template('upload.html')
    


@app.route('/receipts')
def receipts():
    query = db_session.query(Receipt)

    # Search by vendor
    search = request.args.get('search')
    if search:
        query = query.filter(Receipt.vendor.ilike(f"%{search}%"))

    # Filter by date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date:
        query = query.filter(Receipt.date >= start_date)
    if end_date:
        query = query.filter(Receipt.date <= end_date)

    # Sorting
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')
    if sort_by == 'amount':
        query = query.order_by(Receipt.amount.desc() if sort_order == 'desc' else Receipt.amount.asc())
    else:
        query = query.order_by(Receipt.date.desc() if sort_order == 'desc' else Receipt.date.asc())

    receipts = query.all()
    return render_template('receipts.html', receipts=receipts)

@app.route('/confirm', methods=['POST','GET'])
def confirm_data():
    vendor = request.form.get('vendor')
    amount = request.form.get('amount')
    date = request.form.get('date')

    receipt = Receipt(vendor=vendor, amount=float(amount) if amount else None, date=date)
    db_session.add(receipt)
    db_session.commit()

    return redirect(url_for('receipts'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_receipt(id):
    receipt = db_session.query(Receipt).get(id)
    if receipt:
        db_session.delete(receipt)
        db_session.commit()
    return redirect(url_for('receipts'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_receipt(id):
    receipt = db_session.query(Receipt).get(id)
    if not receipt:
        return "Receipt not found", 404

    if request.method == 'POST':
        receipt.vendor = request.form.get('vendor')
        receipt.amount = float(request.form.get('amount')) if request.form.get('amount') else None
        receipt.date = request.form.get('date')
        db_session.commit()
        return redirect(url_for('receipts'))

    return render_template('edit_receipt.html', receipt=receipt)



@app.route('/dashboard')
def dashboard():
    receipts = db_session.query(Receipt).all()

    total = sum(r.amount for r in receipts if r.amount)
    avg = round(total / len(receipts), 2) if receipts else 0

    vendor_totals = defaultdict(float)
    monthly_totals = defaultdict(float)

    for r in receipts:
        if r.amount:
            vendor_totals[r.vendor] += r.amount
        if r.date:
            try:
                dt = datetime.strptime(r.date, '%d/%m/%Y') if '/' in r.date else datetime.strptime(r.date, '%Y-%m-%d')
                key = dt.strftime('%Y-%m')
                monthly_totals[key] += r.amount or 0
            except:
                pass

    # Sort for cleaner charts
    sorted_months = dict(sorted(monthly_totals.items()))
    sorted_vendors = dict(sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True))

    return render_template(
        'dashboard.html',
        total=total,
        avg=avg,
        vendor_totals=sorted_vendors,
        monthly_totals=sorted_months
    )




if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=False)


