# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import random
import datetime

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required

from . import user
from ... import db
from ...models import Member
from ...mem_db import sessionDB, successStr, errorStr, successDataStr, newSession, destorySession, destorySessionAll
from ...email import send_email
from ...common_method import commonMethod
from ...decorators import api_login_required

tool = commonMethod()
@user.route('/Regist', methods=['POST'])
def regist():
    phone_number = request.json.get("phoneNumber")
    password = request.json.get("password")
    member = Member.query.filter_by(phone_number=phone_number).first()
    if member:
        return errorStr(6)
    member = Member(phone_number=phone_number, password=password, creator=0, create_time=datetime.datetime.now())
    db.session.add(member)
    db.session.commit()
    sessionID = newSession(member.id)
    back_obj = {"sessionID":sessionID, 'aboutMe':member.aboutMe()}
    return successDataStr(back_obj)



@user.route('/ChangePassword', methods=['POST'])
def change_password():
    phone_number = request.json.get("phoneNumber")
    password = request.json.get("password")
    member = Member.query.filter_by(phone_number=phone_number).first()
    if member:
        destorySessionAll(memberID=member.id)
        member.password_hash = generate_password_hash(password)
        sessionID = newSession(member.id)
        back_obj = {"sessionID":sessionID, 'aboutMe':member.aboutMe()}
        db.session.commit()

        return successDataStr(back_obj)
    else:
        return errorStr(7)
    
    
@user.route('/ResetPasswordByEmail', methods=['POST'])
def reset_password():
    email = request.json.get("email")

    member = Member.query.filter_by(email=email).first()
    if member:
        destorySessionAll(memberID=member.id)
        sessionID = newSession(member.id)
        token = tool.generate_reset_token("reset", member.id)

        send_email(member.email, 'Reset Your Password',
                   'email/reset_password',
                   user=member, token=token,
                   next=request.args.get('next'))
        back_obj = {"sessionID":sessionID, 'aboutMe':member.aboutMe()}

        return successDataStr(back_obj)
    else:
        return errorStr(7)


 
    
@user.route('/Login', methods=['POST'])
def login():
    user_name = request.json.get("userName")
    password = request.json.get("password")
    sessionID = None
    member = Member.query.filter_by(user_name=user_name).first()
    if member:
        flag = member.verify_password(password)
        if flag:
            sessionID = newSession(member.id)
    else:
        member = Member.query.filter_by(phone_number=user_name).first()
        if member:
            flag = member.verify_password(password)
            if flag:
                sessionID = newSession(member.id)
            flag = member.verify_verification_code(password)
            if flag:
                sessionID = newSession(member.id)
        else:
            member = Member.query.filter_by(email=user_name).first()
            if member:
                flag = member.verify_password(password)
                if flag:
                    sessionID = newSession(member.id)
                flag = member.verify_verification_code(password)

    if sessionID:
        back_obj = {"sessionID":sessionID, 'aboutMe':member.aboutMe()}
        return successDataStr(back_obj)

    
    return errorStr(5)

@user.route('/EmitCode', methods=['GET'])
def emit_code():
    phone_number = request.json.get("phoneNumber")
    verification_code = random.randint(100000,999999)
    # emitcode
    member = Member.query.filter_by(phone_number=phone_number).first()
    if member:
        member.verification_code = str(verification_code)
        member.verification_code_time = int(time.time())
        db.session.commit()
    return '''{"response":{"code":0,"message":""},"verificationCode":"''' + str(verification_code) + '''"}'''

@user.route('/Logout', methods=['GET'])
@api_login_required
def logout():
    sessionID = request.json.get('sessionID')
    destorySession(sessionID)
    return successStr