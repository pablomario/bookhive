
from flask import Blueprint, request, g, jsonify
from blueprints.decorators import require_login
from bson import ObjectId
from pymongo import MongoClient

api_bp = Blueprint('api_bp', __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection_user = db["users"]
collection_books = db["books"]


@api_bp.route('/v1/books/detail/', methods=['GET'])
@require_login
def getBookDetail():
    book_id = request.json.get('book_id')
    book = collection_books.find_one({'_id': ObjectId(book_id)})
    book_cover = getCoverBook(book['cover_reference'])
    book['cover'] = book_cover['book_cover']
    if book:
        return book
    else:
        return jsonify({'error': 'Libro no encontrado'})


@api_bp.route('/v1/books/latest/', methods=['GET'])
@require_login
def getLatestBooks():
    recent_books = collection_books.find().sort('saved_date', -1).limit(7)
    recent_books_list = list(recent_books)
    for book in recent_books_list:
        book['_id'] = str(book['_id'])  # Convertir ObjectId a cadena
        book_cover = getCoverBook(book['cover_reference'])
        book['cover'] = book_cover['book_cover']
    return recent_books_list


def getCoverBook(book_id):
    cover_collection = db['books_cover']
    return cover_collection.find_one({"_id": ObjectId(book_id)})


@api_bp.route('/v1/books/favorite/add', methods=['POST'])
@require_login
def addBookToFavorites():
    try:
        # Obtener el artículo a agregar de la solicitud POST
        book_id = request.json.get('book_id')

        # Verificar si el usuario existe
        user = collection_user.find_one({'_id': ObjectId(g.user["id"])})
        if user:
            # Verificar si el artículo ya está en favoritos
            if book_id in user.get('book_favorites', []):
                return jsonify({'ok': 'El artículo ya está en favoritos'}), 400

            book = collection_books.find_one({'_id': ObjectId(book_id)})
            if book:
                collection_user.update_one({'_id': ObjectId(g.user["id"])},
                                             {'$addToSet': {'book_favorites': ObjectId(book_id)}})
                return jsonify({'ok': 'Libro agregado a favoritos correctamente'})
            else:
                return jsonify({'error': 'El Libro no existe'}), 404
        else:
            return jsonify({'error': 'El usuario no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

