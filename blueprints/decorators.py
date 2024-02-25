from flask import session, redirect, url_for
from functools import wraps


def require_login(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'user_logged' in session:
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('main'))
    return wrapper

