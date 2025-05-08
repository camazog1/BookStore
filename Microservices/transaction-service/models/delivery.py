from extensions import db

class DeliveryProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    coverage_area = db.Column(db.String(150))
    cost = db.Column(db.Float)


class DeliveryAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('delivery_provider.id'))
