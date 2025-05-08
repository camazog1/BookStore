from extensions import db

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # desde el token
    book_id = db.Column(db.Integer, nullable=False)  # verificado en DB
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending Payment')
