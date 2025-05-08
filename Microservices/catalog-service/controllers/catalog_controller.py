from flask import Blueprint, request, jsonify
from extensions import db
from models.book import Book
from flask_jwt_extended import jwt_required, get_jwt_identity

catalog_bp = Blueprint('catalog_bp', __name__)

@catalog_bp.route('/', methods=['GET'])
@jwt_required()
def list_books():
    books = Book.query.all()
    return jsonify([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'description': b.description,
        'price': b.price,
        'stock': b.stock,
        'seller_id': b.seller_id
    } for b in books])

@catalog_bp.route('/my_books', methods=['GET'])
@jwt_required()
def my_books():
    seller_id = int(get_jwt_identity())
    books = Book.query.filter_by(seller_id=seller_id).all()
    return jsonify([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'description': b.description,
        'price': b.price,
        'stock': b.stock
    } for b in books])

@catalog_bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    data = request.json
    seller_id = int(get_jwt_identity())

    book = Book(
        title=data['title'],
        author=data['author'],
        description=data['description'],
        price=float(data['price']),
        stock=int(data['stock']),
        seller_id=int(seller_id)
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added'}), 201

@catalog_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def edit_book(book_id):
    seller_id = int(get_jwt_identity())
    book = Book.query.get_or_404(book_id)

    if book.seller_id != seller_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    book.title = data['title']
    book.author = data['author']
    book.description = data['description']
    book.price = float(data['price'])
    book.stock = int(data['stock'])
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@catalog_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    seller_id = int(get_jwt_identity())
    book = Book.query.get_or_404(book_id)

    if book.seller_id != seller_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})
