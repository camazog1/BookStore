from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.payment import Payment
from models.purchase import Purchase

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/<int:purchase_id>', methods=['POST'])
@jwt_required()
def make_payment(purchase_id):
    user_id = get_jwt_identity()
    data = request.json

    print(f"[DEBUG] JWT user_id: {user_id}")
    print(f"[DEBUG] Incoming JSON: {data}")

    purchase = Purchase.query.get_or_404(purchase_id)
    print(f"[DEBUG] Purchase found: user_id={purchase.user_id}, total_price={purchase.total_price}, status={purchase.status}")

    # Validar que el usuario sea dueño de la compra
    if str(purchase.user_id) != str(user_id):
        print("[ERROR] Unauthorized: user_id mismatch")
        return jsonify({'error': 'Unauthorized'}), 403

    # Validar que no esté ya pagada
    if purchase.status == 'Paid':
        print("[ERROR] Already paid")
        return jsonify({'error': 'Already paid'}), 400

    # Validar campos recibidos
    method = data.get('method')
    if not method:
        print("[ERROR] Missing payment method")
        return jsonify({'error': 'Missing payment method'}), 400

    try:
        amount = float(data.get('amount'))
    except (TypeError, ValueError):
        print(f"[ERROR] Invalid amount received: {data.get('amount')}")
        return jsonify({'error': 'Invalid amount'}), 400

    print(f"[DEBUG] Received amount: {amount} | Expected: {purchase.total_price}")

    if round(amount, 2) != round(purchase.total_price, 2):
        print("[ERROR] Incorrect amount")
        return jsonify({'error': 'Incorrect amount'}), 400

    # Crear pago y actualizar estado de compra
    payment = Payment(
        purchase_id=purchase.id,
        amount=amount,
        payment_method=method,
        payment_status='Paid'
    )

    db.session.add(payment)
    purchase.status = 'Paid'
    db.session.commit()

    print("[SUCCESS] Payment completed")
    return jsonify({'message': 'Payment completed'}), 201
