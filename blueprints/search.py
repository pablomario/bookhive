from flask import Blueprint, render_template, request, g
from pymongo import MongoClient
from bson import ObjectId
from .decorators import require_login
import math, re

search_bp = Blueprint('search_bp', __name__)

# MONGODB CONFIGURATION
client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection = db["books"]


@search_bp.route('/search', methods=['GET', 'POST'])
@require_login
def search():
    if request.method == 'POST':
        keywords = request.form['keywords']

        regex_pattern = re.compile(f'.*{keywords}.*', re.IGNORECASE)
        search_result = collection.find({
            "$or": [
                {"book": {"$regex": regex_pattern}},
                {"author": {"$regex": regex_pattern}}
            ]
        })

        books = list(search_result)
        for book in books:
            book['_id'] = str(book['_id'])
            book_cover = getCoverBook(book['cover_reference'])
            book['cover'] = book_cover['book_cover']
        return render_template('pages/search/search-result.html',
                               books=books)


def getCoverBook(book_id):
    cover_collection = db['books_cover']
    return cover_collection.find_one({"_id": ObjectId(book_id)})