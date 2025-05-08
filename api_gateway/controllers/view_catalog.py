from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
from config import Config

catalog_bp = Blueprint('catalog_bp', __name__)

def auth_headers():
    token = session.get('access_token')
    if not token:
        return {}
    return {'Authorization': f'Bearer {token}'}

@catalog_bp.route('/')
def catalog():
    try:
        res = requests.get(f"{Config.CATALOG_URL}/catalog", headers=auth_headers())
        books = res.json()
        return render_template('catalog.html', books=books)
    except Exception:
        flash('Error al cargar el catálogo', 'danger')
        return render_template('catalog.html', books=[])
    
@catalog_bp.route('/my_books')
def my_books():
    if 'access_token' not in session:
        flash("Debes iniciar sesión para ver tus libros", "warning")
        return redirect(url_for('auth_bp.login'))
    try:
        res = requests.get(f"{Config.CATALOG_URL}/catalog/my_books", headers=auth_headers())
        books = res.json()
        return render_template('my_books.html', books=books)
    except Exception:
        flash("No se pudieron cargar tus libros", "danger")
        return render_template('my_books.html', books=[])

@catalog_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'author': request.form['author'],
            'description': request.form['description'],
            'price': request.form['price'],
            'stock': request.form['stock']
        }
        res = requests.post(f"{Config.CATALOG_URL}/catalog", json=data, headers=auth_headers())
        if res.status_code == 201:
            flash("Libro publicado con éxito", "success")
            return redirect(url_for('catalog_bp.catalog'))
        else:
            flash("Error al publicar el libro", "danger")
    return render_template('add_book.html')

@catalog_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    headers = auth_headers()
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'author': request.form['author'],
            'description': request.form['description'],
            'price': request.form['price'],
            'stock': request.form['stock']
        }
        res = requests.put(f"{Config.CATALOG_URL}/catalog/{book_id}", json=data, headers=headers)
        if res.status_code == 200:
            flash("Libro actualizado", "success")
            return redirect(url_for('catalog_bp.my_books'))
        else:
            flash("Error al actualizar el libro", "danger")

    # Cargar datos actuales del libro (si se necesita prellenar formulario)
    # O puedes omitir esto si el template recibe los datos por otro medio
    return render_template('edit_book.html', book_id=book_id)

@catalog_bp.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'access_token' not in session:
        return redirect(url_for('auth_bp.login'))

    res = requests.delete(f"{Config.CATALOG_URL}/catalog/{book_id}", headers=auth_headers())
    if res.status_code == 200:
        flash("Libro eliminado", "success")
    else:
        flash("No se pudo eliminar el libro", "danger")
    return redirect(url_for('catalog_bp.my_books'))
