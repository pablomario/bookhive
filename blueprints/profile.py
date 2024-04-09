from flask import Blueprint, request, session, redirect, render_template, url_for, g
from pymongo import MongoClient
from bson import ObjectId
from .decorators import require_login

profile_bp = Blueprint('profile_bp', __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["ikawe"]
collection = db["users"]


@profile_bp.route('/profile', methods=['GET'])
@require_login
def page_profile():
    return render_template('pages/profile/profile.html')


@profile_bp.route('/edit-profile', methods=['GET'])
@require_login
def page_update_profile():
    return render_template('pages/profile/update-profile.html')


@profile_bp.route('/edit-profile', methods=['POST'])
@require_login
def update_profile():
    user = collection.find_one({"_id": ObjectId(g.user["id"])})
    if request.form['password'] == user['password']:
        result = collection.update_one({"_id": ObjectId(g.user["id"])}, {
            '$set': {
                'username': request.form['username'],
                'email': request.form['email'],
            }
        })
        if result.modified_count == 1:
            g.user['username'] = request.form['username']
            g.user['email'] = request.form['email']
            ok_message = 'Usuario actualizado correctamente'
            return render_template('pages/profile/update-profile.html',
                                   form_ok=ok_message)
        else:
            error_message = 'Ha ocurrido un error al actualizar el usuario.'
            return render_template('pages/profile/update-profile.html',
                                   form_error=error_message)
    else:
        error_message = 'Ha ocurrido un error al actualizar el usuario.'
        return render_template('pages/profile/update-profile.html',
                               form_error=error_message)