from flask import Blueprint, render_template, request, redirect, url_for
from models.delivery import DeliveryProvider
from extensions import db
from flask_login import login_required
from models.delivery_assignment import DeliveryAssignment
import os

delivery = Blueprint('delivery', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
delivery.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@delivery.route('/delivery/<int:purchase_id>', methods=['GET', 'POST'])
@login_required
def select_delivery(purchase_id):
    providers = DeliveryProvider.query.all()
    if request.method == 'POST':
        selected_provider_id = request.form.get('provider')
        
        if 'delivery_document' in request.files:
            delivery_document = request.files['delivery_document']
            if delivery_document:
                filename = os.path.join(delivery.config['UPLOAD_FOLDER'], delivery_document.filename)
                delivery_document.save(filename)
        
        new_assignment = DeliveryAssignment(purchase_id=purchase_id, provider_id=selected_provider_id, document_path=filename if 'delivery_document' in locals() else None)
        db.session.add(new_assignment)
        db.session.commit()
        
        return redirect(url_for('book.catalog'))
    return render_template('delivery_options.html', providers=providers, purchase_id=purchase_id)
