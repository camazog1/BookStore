from flask import Blueprint, request, jsonify
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.purchase import Purchase
from sqlalchemy import text

purchase_bp = Blueprint('purchase_bp', __name__)

@purchase_bp.route('/<int:book_id>', methods=['POST'])
@jwt_required()
def make_purchase(book_id):
    user_id = get_jwt_identity()
    data = request.json

    quantity = int(data.get('quantity', 1))
    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400

    # Validar existencia del libro directamente en la base de datos compartida
    result = db.session.execute(
        text("SELECT id, price, stock FROM book WHERE id = :book_id"),
        {'book_id': book_id}
    ).fetchone()

    if not result:
        return jsonify({'error': 'Book not found'}), 404

    if result.stock < quantity:
        return jsonify({'error': 'Not enough stock'}), 400

    # Calcular total
    total_price = result.price * quantity

    # Reducir stock
    new_stock = result.stock - quantity
    db.session.execute(
        text("UPDATE book SET stock = :new_stock WHERE id = :book_id"),
        {'new_stock': new_stock, 'book_id': book_id}
    )

    # Crear la compra
    purchase = Purchase(
        user_id=user_id,
        book_id=book_id,
        quantity=quantity,
        total_price=total_price,
        status='Pending Payment'
    )
    db.session.add(purchase)
    db.session.commit()

    return jsonify({'message': 'Purchase created', 'purchase_id': purchase.id}), 201

@purchase_bp.route('/my_purchases', methods=['GET'])
@jwt_required()
def get_my_purchases():
    user_id = get_jwt_identity()
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': p.id,
        'book_id': p.book_id,
        'quantity': p.quantity,
        'total_price': p.total_price,
        'status': p.status
    } for p in purchases])
