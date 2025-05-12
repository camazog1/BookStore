from flask import Flask, render_template
from config import Config
from extensions import jwt
from controllers.view_auth import auth_bp
from controllers.view_catalog import catalog_bp
from controllers.view_transaction import transaction_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar JWT
    jwt.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(transaction_bp)

    # Ruta raíz para mostrar la página principal
    @app.route('/')
    def home():
        return render_template('home.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
