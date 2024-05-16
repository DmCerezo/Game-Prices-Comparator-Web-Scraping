from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db   ##means from __init__.py import db


auth = Blueprint('auth', __name__)


@auth.route('/buscar_juegos')
def buscar_juegos():
    return render_template("buscar_juegos.html")

@auth.route('/')
def inicio():
    return render_template("inicio.html")

@auth.route('/info')
def info():
    return render_template("info.html")
