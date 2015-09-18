from flask import Blueprint

team_manage = Blueprint('team_manage', __name__)

from . import views
