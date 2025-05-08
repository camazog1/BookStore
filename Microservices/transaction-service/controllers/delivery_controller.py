from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.purchase import Purchase
from models.delivery import DeliveryProvider, DeliveryAssignment

delivery_bp = Blueprint('delivery_bp', __name__)

@delivery_bp.route('/providers', methods=['GET'])
def list_providers():
    providers = DeliveryProvider.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'coverage_area': p.coverage_area,
        'cost': p.cost
    } for p in providers])

@delivery_bp.route('/<int:purchase_id>', methods=['POST'])
@jwt_required()
def assign_delivery(purchase_id):
    user_id = get_jwt_identity()
    data = request.json

    provider_id = data.get('provider_id')
    if not provider_id:
        return jsonify({'error': 'Missing provider_id'}), 400

    # Verificar que la compra existe y pertenece al usuario
    purchase = Purchase.query.get_or_404(purchase_id)
    if str(purchase.user_id) != str(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Verificar que el proveedor existe
    provider = DeliveryProvider.query.get(provider_id)
    if not provider:
        return jsonify({'error': 'Invalid provider_id'}), 404

    # Crear la asignación
    assignment = DeliveryAssignment(
        purchase_id=purchase_id,
        provider_id=provider_id
    )
    db.session.add(assignment)
    db.session.commit()

    return jsonify({'message': 'Delivery provider assigned'}), 201
