from flask import Blueprint

user_manage = Blueprint('user_manage', __name__)

from . import views
