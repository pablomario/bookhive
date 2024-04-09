
from flask import Blueprint, request, g, jsonify
from blueprints.decorators import require_login
from bson import ObjectId
from pymongo import MongoClient

api_bp = Blueprint('api_bp', __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection_user = db["users"]
collection_books = db["books"]


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

