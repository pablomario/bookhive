from flask import Blueprint, request, session, redirect, render_template, url_for
from .decorators import require_login

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/profile', methods=['GET'])
@require_login
def page_profile():
    # TODO - Update Profile page
    return render_template('pages/profile/profile.html')

