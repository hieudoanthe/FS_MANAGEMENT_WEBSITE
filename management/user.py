from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages, jsonify
from sqlalchemy.sql.expression import false
from management.models import User, Note, Product, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from management import db

user = Blueprint("user", __name__)

@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user, remember=True)
                flash("Logged in successfully!", category="success")

                # Kiểm tra nếu có trang tiếp theo (next page) đã được đặt trong session
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)

                # Nếu không có trang 'next', chuyển hướng đến trang chính (home)
                return redirect(url_for("views.home"))
            else:
                flash("Password is wrong :)", category="error")
        else:
            flash("User doesn't exist!", category="error")
    messages = get_flashed_messages()
    return render_template("login.html", user=current_user)

@user.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        user = User.query.filter_by(email = email).first()
        if user:
            flash("User existed !", category="error")
        elif len(email) < 4:
            flash("Email sort !", category="error")
        elif len(password) < 7:
            flash("Password sort !",category="error")
        elif password != confirm_password:
            flash("Password does not match !",category="error")
        else:  
            password = generate_password_hash(password, method="sha256")
            new_user = User(email=email, password=password, user_name=user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                flash("User created !", category="success")
                return redirect(url_for("views.home"))   
            except:
                "error"
    messages = get_flashed_messages()
    return render_template("signup.html", user=current_user)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))


@user.route("/save_checkout", methods=["POST"])
@login_required
def save_checkout():
    try:
        # Nhận dữ liệu từ request
        data = request.get_json()

        # Lưu thông tin sản phẩm vào cơ sở dữ liệu
        save_products_to_database(data['products'])

        # Trả về thông báo thành công
        return jsonify({'message': 'Checkout successful'}), 200

    except Exception as e:
        print(str(e))
        # Trả về thông báo lỗi
        return jsonify({'error': 'An error occurred'}), 500

# Hàm lưu thông tin sản phẩm vào cơ sở dữ liệu
def save_products_to_database(products):
    for product in products:
        # Thực hiện lưu thông tin sản phẩm vào cơ sở dữ liệu (sử dụng SQLAlchemy)
        # new_product = Product(name="2023 new long-sleeved shirts", total_price="130.00", user_id=1)
        new_product = Product(name=product['name'], total_price=product['price'], user_id=current_user.id)
        db.session.add(new_product)
        db.session.commit()


@user.route("/admin_login",methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        adminName = request.form.get("adminName")
        password = request.form.get("adminPass")
        admin = Admin.query.filter_by(admin_name=adminName).first()
        if admin:
            if check_password_hash(admin.password, password):
                session.permanent = True
                login_user(admin,remember=True)
                flash("Logged is success !",category="success")
                return redirect(url_for("views.management_dashboard"))
            else:
                flash("Password is wrong :)",category="error")
        else:
            flash("User doesn't exist !",category="error")
    messages = get_flashed_messages()
    return render_template("admin_login.html", user = current_user)
