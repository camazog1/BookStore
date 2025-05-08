from flask import Blueprint, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from extensions import db
from models.purchase import Purchase
from models.book import Book
from flask_login import login_required, current_user

purchase = Blueprint('purchase', __name__)

UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@purchase.route('/buy/<int:book_id>', methods=['POST'])
@login_required
def buy(book_id):
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))

    book = Book.query.get_or_404(book_id)

    if book.stock < quantity:
        return "No hay suficiente stock disponible.", 400

    total_price = price * quantity

    new_purchase = Purchase(
        user_id=current_user.id,
        book_id=book_id,
        quantity=quantity,
        total_price=total_price,
        status='Pending Payment'
    )
    book.stock -= quantity  # Reducir stock
    db.session.add(new_purchase)
    db.session.commit()

    if 'receipt' in request.files:
        file = request.files['receipt']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)  

            new_purchase.receipt_path = file_path
            db.session.commit()

    return redirect(url_for('payment.payment_page', purchase_id=new_purchase.id))
