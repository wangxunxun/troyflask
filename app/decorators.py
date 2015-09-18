# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from functools import wraps
import time

from flask import abort, request
from flask_login import current_user
from mem_db import sessionDB
from config import Config
from .models import Permission

def api_login_required(func):
    @wraps(func)
    def check_session(*args, **kwargs):
        sessionID = request.json.get('sessionID')
        if sessionID is None:
            sessionID = request.json.get('sessionID')
        if sessionID:
            if sessionID in sessionDB:
                if time.time() - sessionDB[sessionID]['update_time'] > Config.API_SESSION_TIME_OUT:
                    sessionDB.pop(sessionID)
                    return '''{"response":{"code":1,"message":"Session过期,请重新登录"}}'''
                else:
                    sessionDB[sessionID]['update_time'] = time.time()
                    return func(*args, **kwargs)
            else:
                return '''{"response":{"code":4,"message":"您的请求被拒绝,Session失效，请先登录"}}'''
        else:
            return '''{"response":{"code":4,"message":"请的请求被拒绝,请先登录"}}'''

    return check_session



def server_permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def server_admin_required(f):
    return server_permission_required(Permission.ADMINISTER)(f)
