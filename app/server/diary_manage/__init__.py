from flask import Blueprint

diary_manage = Blueprint('diary_manage', __name__)

from . import views
