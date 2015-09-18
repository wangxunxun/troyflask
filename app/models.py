# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from . import db
from . import login_manager
from flask_login import UserMixin,AnonymousUserMixin
import datetime


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(45))
    user_name = db.Column(db.String(45))
    password_hash = db.Column(db.String(100))
    verification_code = db.Column(db.String(15))
    verification_code_time = db.Column(db.Integer)
    sex = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    real_name = db.Column(db.String(45))
#    img = db.Column(db.ForeignKey(u'resources.id'), index=True)
    id_card_No = db.Column(db.String(45))
    intro = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, nullable=False)
#    update_time = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    creator = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

#    resource = db.relationship(u'Resource')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_verification_code(self, password):
        if self.verification_code and self.verification_code_time:
            return self.verification_code == password and time.time() - self.verification_code_time < 60
        else:
            return False


    
    def reset_password(self,new_password):
        self.password = new_password
        db.session.add(self)
   
    

    def aboutMe(self):
        aboutMe = {}
        aboutMe['userId'] = self.id
        aboutMe['userName'] = self.user_name
        aboutMe['email'] = self.email
        aboutMe['trueName'] = self.real_name
        aboutMe['sex'] = self.sex
        aboutMe['phone'] = self.phone_number
        aboutMe['IDCardNo'] = self.id_card_No
        aboutMe['intro'] = self.intro
#        if self.resource:
#            aboutMe['profileImage'] = self.resource.compressed_file_url
#        else:
#            aboutMe['profileImage'] = None

        return aboutMe
    
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    explain = db.Column(db.String(500), nullable=False, server_default=db.text("'Explain...'"))
    create_time = db.Column(db.DateTime, nullable=False)
#    update_time = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    creator = db.Column(db.String(45), nullable=False,server_default=db.text("'0'"))
    is_deleted = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.create_time = datetime.datetime.now()
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    user_name = db.Column(db.String(45), nullable=False)
    password_hash = db.Column(db.String(100))
    verification_code = db.Column(db.String(15))
    verification_code_time = db.Column(db.Integer)
    sex = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    real_name = db.Column(db.String(45))
#    img = db.Column(db.ForeignKey(u'resources.id'), index=True)
    id_card_No = db.Column(db.String(45))
    intro = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, nullable=False)
#    update_time = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    creator = db.Column(db.Integer, nullable=False,server_default=db.text("'0'"))
    is_deleted = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    diarys = db.relationship('Diary', backref='user', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()

                
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    
    
    
class Diary(db.Model):
    __tablename__ = 'diarys'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(500), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

    
    
    
    
    
    
    
    
    
    
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser        
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))