from flask import Blueprint, request, render_template
from pymongo import MongoClient
from bson import ObjectId
from blueprints.decorators import require_login

edit_book_bp = Blueprint('edit_book_bp', __name__)

# MONGODB CONFIGURATION
client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection = db["books"]


def getCoverBook(book_id):
    cover_collection = db['books_cover']
    return cover_collection.find_one({"_id": ObjectId(book_id)})


@edit_book_bp.route('/book/<string:book_id>', methods=['GET'])
@require_login
def page_edit_book(book_id):
    book = collection.find_one({"_id": ObjectId(book_id)})
    book_cover = getCoverBook(book['cover_reference'])
    book['cover'] = book_cover['book_cover']
    book['book_id'] = book_id
    # TODO - Detectar si el libro no está publicado
    if book:
        return render_template('pages/admin/edit-book.html', book=book)
    else:
        return render_template('404.html')


@edit_book_bp.route('/book/<string:book_id>', methods=['POST'])
@require_login
def edit_book(book_id):
    action = request.form.get('action')

    if action == 'edit':
        result = collection.update_one({"_id": ObjectId(book_id)}, {
            '$set': {
                'book': request.form['book-title'],
                'author': request.form['book-author'],
                'theme': request.form['book-theme'],
                'year': request.form['book-year'],
                'summary': request.form['book-summary'],
                'status': 1
            }
        })
        book = collection.find_one({"_id": ObjectId(book_id)})
        if result.modified_count == 1:
            ok_message = 'Libro Actualizado exitosamente.'
            return render_template('pages/admin/edit-book.html',
                                   book=book,
                                   form_ok=ok_message)
        else:
            error_message = 'Ha ocurrido un error al actualizar el libro.'
            return render_template('pages/admin/edit-book.html',
                                   book=book,
                                   form_error=error_message)
    elif action == 'delete':
        result = collection.update_one({"_id": ObjectId(book_id)}, {
            '$set': {
                'status': -1
            }
        })
        book = collection.find_one({"_id": ObjectId(book_id)})
        if result.modified_count == 1:
            ok_message = 'Libro Eliminado exitosamente.'
            return render_template('pages/admin/edit-book.html',
                                   book=book,
                                   form_ok=ok_message)
        else:
            error_message = 'Ha ocurrido un error al actualizar el libro.'
            return render_template('pages/admin/edit-book.html',
                                   book=book,
                                   form_error=error_message)

