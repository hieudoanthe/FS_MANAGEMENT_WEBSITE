from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages, jsonify
from sqlalchemy.sql.expression import false
from management.models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from management import db

views = Blueprint("views", __name__)


@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])
@login_required
def home():
    return render_template("index.html")

@views.route('/details')
def shop_details():
    return render_template('detail.html')

@views.route('/cart')
def shop_cart():
    return render_template('cart.html')

@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def shop_checkout():
    return render_template('checkout.html')

@views.route('/contact')
def shop_contact():
    return render_template('contact.html')

@views.route('/shop')
def shop_ourShop():
    return render_template('shop.html')