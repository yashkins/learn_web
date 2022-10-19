from flask import Blueprint, render_template
from webapp.db import db

blueprint = Blueprint('error', __name__)

@blueprint.app_errorhandler(404)
def not_found_error(error):
    title = "Ой, кажется что-то пошло не так!"
    return render_template('error/error.html', page_title=title), 404

@blueprint.app_errorhandler(500)
def internal_error(error):
    title = "Ой, кажется что-то пошло не так!"
    db.session.rollback()
    return render_template('error/error.html', page_title=title), 500

