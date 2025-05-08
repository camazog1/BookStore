from flask import Blueprint, render_template, request, redirect, url_for
from models.payment import Payment
from models.purchase import Purchase
from extensions import db
from flask_login import login_required
import os

payment = Blueprint('payment', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
payment.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@payment.route('/payment/<int:purchase_id>', methods=['GET', 'POST'])
@login_required
def payment_page(purchase_id):
    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')
        
        if 'payment_receipt' in request.files:
            receipt_file = request.files['payment_receipt']
            if receipt_file:
                filename = os.path.join(payment.config['UPLOAD_FOLDER'], receipt_file.filename)
                receipt_file.save(filename)
        else:
            filename = None
        
        new_payment = Payment(purchase_id=purchase_id, amount=amount, payment_method=method, payment_status='Paid', receipt_path=filename)
        db.session.add(new_payment)

        purchase = Purchase.query.get(purchase_id)
        purchase.status = 'Paid'
        db.session.commit()

        return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))
    
    return render_template('payment.html', purchase_id=purchase_id)
