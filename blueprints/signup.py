from flask import Blueprint, request, render_template
from pymongo import MongoClient

signup_bp = Blueprint('signup_bp', __name__)

# MONGODB CONFIGURATION
client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection = db["users"]


@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error_message = 'Email and Password can not Empty'
            return render_template('pages/signup/register.html',
                                   form_error=error_message)

        new_user = {
            "rol": "user",
            "avatar": "",
            "username": username,
            "email": email,
            "password": password,
        }

        try:
            result = collection.insert_one(new_user)
            if result.acknowledged:
                ok_message = 'Registro completado! Ya puedes iniciar sesión.'
                return render_template('pages/signup/register.html',
                                       form_ok=ok_message)
            else:
                error_message = 'Error registering user. Try it again later.'
                return render_template('pages/signup/register.html',
                                       form_error=error_message)
        except Exception as e:
            error_message = f'Exception captured {str(e)}'
            return render_template('pages/signup/register.html',
                                   form_error=error_message)

    return render_template('pages/signup/register.html')


@signup_bp.route('/confirmation')
def signup_confirm():
    return render_template('pages/signup/confirm.html')
