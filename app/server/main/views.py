from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response

from . import main
from ... import db



@main.route('/Index')

def index():
    return render_template('index.html')


@main.route('/')

def _index():
    return redirect(url_for('main.index'))