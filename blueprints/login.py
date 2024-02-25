from flask import Blueprint, request, session, redirect, render_template, url_for
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection = db["dashboard"]

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = db['users']
        user_logged = users.find_one({'email': email, 'password': password})

        if user_logged:
            user_logged_data = {
                'username': user_logged['username'],
                'email': user_logged['email'],
                'rol': user_logged['rol']
            }
            session.clear()
            session['user_logged'] = user_logged_data
            return redirect(url_for('dashboard_bp.page_dashboard'))
        else:
            error_message = "User not valid"
            return render_template('index.html', error=error_message)
    return render_template('index.html')


@login_bp.route('/logout')
def logout():
    session.pop('user_logged', None)
    return redirect(url_for('main'))
