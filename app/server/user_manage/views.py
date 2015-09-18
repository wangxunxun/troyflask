# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for,current_app
from . import user_manage
from ...models import db,Role,User
from ...models import Member
from flask_login import login_user,logout_user,login_required,current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.helpers import flash
from ...common_method import commonMethod
import datetime

tool = commonMethod()


@user_manage.route('/initialsql', methods=['GET', 'POST'])
def initial_sql():
    if request.method == 'POST':
        db.drop_all()
        db.create_all() 
        Role.insert_roles()

    return render_template('success.html')

@user_manage.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        phone_number = request.form.get("phone")
        email = request.form.get("email")
        user_name = request.form.get("username")
        realname = request.form.get("realname")
        password = request.form.get("password")
        if len(password)<6 or len(password)>30:
            flash(u"密码应大于6小于30个字符")
        elif User.query.filter_by(phone_number = phone_number).first():
            flash(u"该手机号已注册")
        elif User.query.filter_by(email = email).first():
            flash(u"该邮箱已注册")
        elif User.query.filter_by(user_name = user_name).first():
            flash(u"该用户名已注册")
        else:

            user = User(phone_number = phone_number,email = email, user_name = user_name,
                        real_name = realname,password = password,create_time = datetime.datetime.now(),role_id = 3)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user_manage.login'))
         
    return render_template('regist.html')

@user_manage.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(phone_number = username).first()
        if user:
            if user.verify_password(password):
                login_user(user)
                return redirect(url_for('main.index'))

            else:
                flash(u"密码错误")
        elif User.query.filter_by(email = username).first():
            user = User.query.filter_by(email = username).first()
            if user.verify_password(password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash(u"密码错误")
            
        elif User.query.filter_by(user_name = username).first():
            user = User.query.filter_by(user_name = username).first()
            if user.verify_password(password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash(u"密码错误")
        else:
            flash(u"用户名或密码错误")
            

         
    return render_template('login.html')

@user_manage.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('user_manage.login'))

@user_manage.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):


    if request.method == 'POST':
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if len(password)<6:
            flash(u"密码需大于6个字符")
        elif len(password)>30:
            flash(u"密码需小于30个字符")
        elif password2 !=password:
            flash(u"确认密码和密码不相同")
        else:
            id = tool.load_token(token).get("reset")
            print(id)
#            id = load_token(token)
            user = Member.query.filter_by(id=id).first()
            user.reset_password(password)
            return redirect(url_for('user_manage.login'))


    return render_template('reset_password.html')  