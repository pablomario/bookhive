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
    if book:
        return render_template('pages/admin/edit-book.html', book=book)
    else:
        return render_template('404.html')
