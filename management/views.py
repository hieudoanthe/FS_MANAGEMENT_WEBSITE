from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages, jsonify
from sqlalchemy.sql.expression import false
from management.models import User, Note, Order
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
    if request.method == 'POST':
        # Lấy giỏ hàng từ local storage
        cart = request.json.get('cart')
        if not cart:
            return jsonify({'error': 'Invalid data format'}), 400
     # Lấy thông tin sản phẩm và giá từ request hoặc từ dữ liệu gửi lên
        product_name = request.json.get('product_name')
        total_price = request.json.get('total_price')
        # Tạo một đối tượng Order và thêm vào cơ sở dữ liệu
        new_order = Order(product_name=product_name, total_price=total_price, user=current_user)
        db.session.add(new_order)
        db.session.flush()

        # Duyệt qua các sản phẩm trong giỏ hàng và thêm vào cơ sở dữ liệu
        for product in cart:
            # Tạo một đối tượng Note và thêm vào cơ sở dữ liệu
            new_note = Order(data=product['name'], order=new_order)
            db.session.add(new_note)

        # Commit để lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()

        flash('Order placed successfully!', 'success')

        # Gửi phản hồi về trình duyệt để xóa giỏ hàng
        return jsonify({'success': True})

    # Nếu là GET request, hiển thị trang checkout bình thường
    return render_template('checkout.html')

@views.route('/contact')
def shop_contact():
    return render_template('contact.html')

@views.route('/shop')
def shop_ourShop():
    return render_template('shop.html')