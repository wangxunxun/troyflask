# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for,current_app,g
from ...models import db,Permission,Diary

from . import diary_manage
from flask_login import login_user,logout_user,login_required,current_user
from flask.helpers import flash
from ...common_method import commonMethod
import datetime
from ...decorators import server_admin_required,server_permission_required




@diary_manage.route('/add_dairy', methods=['GET', 'POST'])
@login_required
def addDiary():
    if request.method == 'POST':
        current_user.id
        title = request.form.get("title")
        body = request.form.get("body")
        diary = Diary(title = title,body = body,userid = current_user.id,create_time = datetime.datetime.now())
        db.session.add(diary)
        db.session.commit()

    return render_template('diary/create_diary.html')

@diary_manage.route('/edit_diary/<id>', methods=['GET', 'POST'])
@login_required
@server_admin_required
def editDiary(id):
    if request.method == 'POST':
        diary = Diary.query.filter_by(id = id).first()
        title = request.form.get("title")
        body = request.form.get("body")
        diary.title = title
        diary.body = body
        db.session.add(diary)
        db.session.commit()
        return redirect(url_for('diary_manage.diaryManage'))

    return render_template('diary/edit_diary.html')

@diary_manage.route('/edit_my_diary/<id>', methods=['GET', 'POST'])
@login_required
def editMyDiary(id):
    if request.method == 'POST':
        diary = Diary.query.filter_by(id = id).first()
        title = request.form.get("title")
        body = request.form.get("body")
        diary.title = title
        diary.body = body
        db.session.add(diary)
        db.session.commit()
        return redirect(url_for('diary_manage.myDiary'))

    return render_template('diary/edit_diary.html')



@diary_manage.route('/diary_manage', methods=['GET', 'POST'])
@login_required
@server_admin_required
def diaryManage():
    diarys = Diary.query.all()
    return render_template('diary/diary_manage.html',diarys = diarys)

@diary_manage.route('/delete_diary/<id>', methods=['GET', 'POST'])
@login_required
@server_admin_required
def deleteDiary(id):

    diary = Diary.query.filter_by(id = id).first()
    db.session.delete(diary)
    db.session.commit()
    return redirect(url_for('diary_manage.diaryManage'))

@diary_manage.route('/my_diary', methods=['GET', 'POST'])
@login_required
def myDiary():
    diarys = Diary.query.filter_by(userid = current_user.id).all()
    for diary in diarys:
        print(diary.create_time)
        print(diary.create_time.strftime("%Y-%m-%d %H:%M:%S"))
    return render_template('diary/my_diary_manage.html',diarys = diarys)

@diary_manage.route('/delete_my_diary/<id>', methods=['GET', 'POST'])
@login_required
def deleteMyDiary(id):

    diary = Diary.query.filter_by(id = id).first()
    db.session.delete(diary)
    db.session.commit()
    return redirect(url_for('diary_manage.myDiary'))

