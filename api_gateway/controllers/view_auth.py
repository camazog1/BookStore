from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from config import Config

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            response = requests.post(f"{Config.AUTH_URL}/auth/login", json={
                'email': email,
                'password': password
            })
            if response.status_code == 200:
                data = response.json()
                session['access_token'] = data['access_token']
                flash('Login successful', 'success')
                return redirect(url_for('catalog_bp.catalog'))
            else:
                flash('Login failed', 'danger')
        except Exception as e:
            flash('Connection error', 'danger')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            response = requests.post(f"{Config.AUTH_URL}/auth/register", json={
                'name': name,
                'email': email,
                'password': password
            })
            if response.status_code == 201:
                flash('User registered successfully', 'success')
                return redirect(url_for('auth_bp.login'))
            else:
                flash('Registration failed', 'danger')
        except Exception as e:
            flash('Connection error', 'danger')
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('auth_bp.login'))
