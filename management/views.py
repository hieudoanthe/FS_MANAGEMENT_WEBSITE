from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages, jsonify
from sqlalchemy.sql.expression import false
from management.models import User, Note, Product, Order
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from management import db
from sqlalchemy import func

views = Blueprint("views", __name__)

# Trang chủ 
@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])
@login_required
def home():
    return render_template("index.html")
# Chi tiết 
@views.route('/details')
def shop_details():
    return render_template('detail.html')
# Giỏ hàng
@views.route('/cart')
def shop_cart():
    return render_template('cart.html')
# Thanh toán
@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def shop_checkout():
    products = Product.query.all()

    # Tính tổng giá tiền của các sản phẩm trong Python
    total_price = sum(product.total_price for product in products)

    return render_template('checkout.html', products=products, total_price=total_price)
# Thanh toán: Xóa sản phẩm 
@views.route('/checkout/<int:product_id>', methods=['DELETE'])
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
# Liên hệ 
@views.route('/contact')
def shop_contact():
    return render_template('contact.html')
# Mua hàng
@views.route('/shop')
def shop_ourShop():
    return render_template('shop.html')
# Khi ấn hủy thực hiện xóa sản phẩm khỏi cơ sở dữ liệu nếu có
@views.route('/clear_cart_on_cancel', methods=['POST'])
@login_required
def clear_cart_on_cancel():
    try:
        # Lấy ID của người dùng hiện tại
        user_id = current_user.id

        # Kiểm tra xem có sản phẩm trong giỏ hàng của người dùng hay không
        product_count = db.session.query(func.count(Product.id)).filter_by(user_id=user_id).scalar()

        if product_count > 0:
            # Nếu có sản phẩm, thực hiện xóa toàn bộ sản phẩm của người dùng trong bảng product
            db.session.query(Product).filter_by(user_id=user_id).delete()
            db.session.commit()

            return jsonify({'success': True, 'message': 'Đã xóa toàn bộ sản phẩm của người dùng'})
        else:
            return jsonify({'success': False, 'message': 'Không có sản phẩm để xóa'})
    except Exception as e:
        # Xử lý lỗi nếu có
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@views.route('/submit_order', methods=['POST'])
def submit_order():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    phoneNumber = request.form.get('phoneNumber')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zipCode = request.form.get('zipCode')
    payment_method = request.form.get('payment_method')
    total_price = float(request.form.get('totalPrice'))

    # Lưu thông tin đơn hàng vào cơ sở dữ liệu
    new_order = Order(
        first_name=first_name,
        last_name=last_name,
        email = email,
        phone_number = phoneNumber,
        payment_method=payment_method,
        address = address,
        city = city,
        state = state,
        zip_code = zipCode,
        total_price = total_price
    )

    db.session.add(new_order)
    db.session.commit()

    # Thực hiện logic cho việc chọn phương thức thanh toán (Paypal, Direct Check, Bank Transfer)
    # (Có thể chuyển hướng hoặc hiển thị thông báo thành công tùy thuộc vào yêu cầu của bạn)

    if payment_method == 'paypal':
        return redirect('https://www.paypal.com/checkoutnow/error?token=EC-6Y751523CE697722J')
    elif payment_method == 'directcheck':
        return render_template('directcheck.html', order=new_order)
    elif payment_method == 'banktransfer':
        # Nếu có trang riêng cho bank transfer, thì thay đổi đường dẫn và template
        return render_template('banktransfer.html', order=new_order)


# Admin 
@views.route('/dashboard')
@views.route('/management_dashboard')
@login_required
def management_dashboard():
    return render_template('p_dashboard.html')