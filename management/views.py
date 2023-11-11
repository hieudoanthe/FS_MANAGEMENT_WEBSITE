from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages, jsonify
from sqlalchemy.sql.expression import false
from management.models import User, Note, Product
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

# @views.route('/cart')
# def shop_cart():
#     return render_template('cart.html')

@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def shop_checkout():
    products = Product.query.all()  # Lấy tất cả sản phẩm từ cơ sở dữ liệu
    return render_template('checkout.html', products=products)

@views.route('/contact')
def shop_contact():
    return render_template('contact.html')

@views.route('/shop')
def shop_ourShop():
    return render_template('shop.html')

@views.route('/cart')
def shop_cart():
    # Lấy sản phẩm từ cơ sở dữ liệu để hiển thị trên giỏ hàng
    products = Product.query.all()
    return render_template('cart.html', products=products)

@views.route('/cart/<int:product_id>', methods=['DELETE'])
@login_required
def remove_product_from_cart(product_id):
    try:
        # Lấy sản phẩm từ cơ sở dữ liệu
        product = Product.query.get(product_id)

        if product:
            # Xóa sản phẩm khỏi cơ sở dữ liệu
            db.session.delete(product)
            db.session.commit()

            return jsonify({"success": True, "message": "Xóa sản phẩm thành công"})
        else:
            return jsonify({"success": False, "message": "Không tìm thấy sản phẩm"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
