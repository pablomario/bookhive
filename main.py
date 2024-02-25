from flask import Flask, g, session, render_template
from pymongo import MongoClient
from blueprints.login import login_bp
from blueprints.signup import signup_bp
from blueprints.dashboard import dashboard_bp
from blueprints.profile import profile_bp
from blueprints.search import search_bp
from blueprints.admin.editBook import edit_book_bp

# APP CONFIGURATION
app = Flask(__name__)
app.secret_key = 'secret_123*'

# APP ROUTES CONFIGURATION
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(edit_book_bp, url_prefix='/admin/edit')


total_books = None


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html',
                           custom_navbar_style=True)


@app.before_request
def before_request():
    initialize_total_books()
    g.user = session.get('user_logged', {})


# ERROR 404 ---------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# UTILS ---------------------
@app.template_filter('truncate_text')
def truncate_text(s, length):
    if len(s) <= length:
        return s
    else:
        return s[:length] + '...'


def initialize_total_books():
    global total_books
    if total_books is None:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["ikawe"]
        collection = db["books"]
        total_books = collection.count_documents({})  # total_books como variable local
    g.total_books = total_books


with app.app_context():
    initialize_total_books()

if __name__ == '__main__':
    app.run(debug=True)
