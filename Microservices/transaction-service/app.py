from flask import Flask
from config import Config
from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Importar y registrar blueprints
    from controllers.purchase_controller import purchase_bp
    from controllers.payment_controller import payment_bp
    from controllers.delivery_controller import delivery_bp

    app.register_blueprint(purchase_bp, url_prefix='/purchase')
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(delivery_bp, url_prefix='/delivery')

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
