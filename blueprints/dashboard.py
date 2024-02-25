import math
import pymongo
from bson import ObjectId
from flask import Blueprint, render_template, request, g, send_from_directory
from pymongo import MongoClient
from .decorators import require_login

dashboard_bp = Blueprint('dashboard_bp', __name__)

# MONGODB CONFIGURATION
client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection = db["books"]


@dashboard_bp.route('/', methods=['GET'])
@require_login
def page_dashboard():
    page = request.args.get('page', default=1, type=int)
    books_per_page = 25
    total_pages = math.ceil(g.total_books / books_per_page)
    skip = (page - 1) * books_per_page
    books = list(collection.find({})
                 .skip(skip)
                 .sort('saved_date', pymongo.DESCENDING)
                 .limit(books_per_page))

    for book in books:
        book['_id'] = str(book['_id'])
        book_cover = getCoverBook(book['cover_reference'])
        book['cover'] = book_cover['book_cover']
    return render_template('pages/dashboard/dashboard.html',
                           books=books,
                           page=page,
                           total_pages=total_pages)


def getCoverBook(book_id):
    cover_collection = db['books_cover']
    return cover_collection.find_one({"_id": ObjectId(book_id)})


@dashboard_bp.route('/detail/<string:book_id>', methods=['GET'])
@require_login
def page_book(book_id):
    book = collection.find_one({"_id": ObjectId(book_id)})
    book_cover = getCoverBook(book['cover_reference'])
    book['cover'] = book_cover['book_cover']
    if book:
        book['_id'] = str(book['_id'])
        return render_template('pages/dashboard/detail.html', book=book)
    else:
        return render_template('404.html')


@dashboard_bp.route('/detail/download/<filename>/<book_name>')
@require_login
def download_file(filename, book_name):
    custom_name = book_name.replace(' ', '_') + '.mobi'
    return send_from_directory('static/ebooks', filename, as_attachment=True, download_name=custom_name)
