from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
from config import Config

transaction_bp = Blueprint('transaction_bp', __name__)

def auth_headers():
    token = session.get('access_token')
    if not token:
        return {}
    return {'Authorization': f'Bearer {token}'}

@transaction_bp.route('/purchase/<int:book_id>', methods=['POST'])
def purchase_book(book_id):
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    quantity = request.form.get('quantity', 1)
    try:
        res = requests.post(
            f"{Config.TRANSACTION_URL}/purchase/{book_id}",
            json={'quantity': quantity},
            headers=auth_headers()
        )
        if res.status_code == 201:
            purchase_id = res.json()['purchase_id']
            flash("Compra iniciada", "success")
            return redirect(url_for('transaction_bp.payment', purchase_id=purchase_id))
        else:
            flash("Error al realizar la compra", "danger")
    except Exception:
        flash("Error de conexión", "danger")

    return redirect(url_for('catalog_bp.catalog'))

@transaction_bp.route('/payment/<int:purchase_id>', methods=['GET', 'POST'])
def payment(purchase_id):
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    headers = auth_headers()

    if request.method == 'POST':
        method = request.form['method']
        amount = float(request.form['amount'])  # aseguramos que sea float

        try:
            res = requests.post(
                f"{Config.TRANSACTION_URL}/payment/{purchase_id}",
                json={'amount': amount, 'method': method},
                headers=headers
            )
            if res.status_code == 201:
                flash("Pago exitoso", "success")
                return redirect(url_for('transaction_bp.delivery', purchase_id=purchase_id))
            else:
                flash("Error en el pago", "danger")
        except Exception:
            flash("Error de conexión", "danger")

    # GET: cargar monto real desde microservicio
    try:
        purchase_res = requests.get(
            f"{Config.TRANSACTION_URL}/purchase/my_purchases",
            headers=headers
        )
        purchases = purchase_res.json()
        purchase = next((p for p in purchases if p['id'] == purchase_id), None)
        if not purchase:
            flash("Compra no encontrada", "danger")
            return redirect(url_for('catalog_bp.catalog'))
        total_price = purchase['total_price']
    except Exception:
        flash("Error al obtener información de la compra", "danger")
        total_price = 0

    return render_template('payment.html', purchase_id=purchase_id, total_price=total_price)


@transaction_bp.route('/delivery/<int:purchase_id>', methods=['GET', 'POST'])
def delivery(purchase_id):
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    if request.method == 'POST':
        provider_id = request.form['provider']
        res = requests.post(
            f"{Config.TRANSACTION_URL}/delivery/{purchase_id}",
            json={'provider_id': provider_id},
            headers=auth_headers()
        )
        if res.status_code == 201:
            flash("Entrega asignada", "success")
            return redirect(url_for('catalog_bp.catalog'))
        else:
            flash("Error al asignar proveedor", "danger")

    try:
        res = requests.get(f"{Config.TRANSACTION_URL}/delivery/providers")
        providers = res.json()
    except Exception:
        flash("No se pudieron cargar proveedores", "danger")
        providers = []

    return render_template('delivery_options.html', providers=providers, purchase_id=purchase_id)

@transaction_bp.route('/my_purchases')
def my_purchases():
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    try:
        res = requests.get(
            f"{Config.TRANSACTION_URL}/purchase/my_purchases",
            headers=auth_headers()
        )
        purchases = res.json()
        return render_template('my_purchases.html', purchases=purchases)
    except Exception:
        flash("Error al obtener tus compras", "danger")
        return render_template('my_purchases.html', purchases=[])
