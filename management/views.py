from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages, jsonify, send_file
from sqlalchemy.sql.expression import false
from management.models import User, Note, Product, Order, Amin_addProduct
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from management import db
from sqlalchemy import func
from datetime import datetime, timedelta
from flask import make_response
import qrcode
from PIL import Image
import os
from io import BytesIO

if not os.path.exists('qrcodes'):
    os.makedirs('qrcodes')

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
        return redirect(url_for('views.show_qr', order_id=new_order.id))
    elif payment_method == 'banktransfer':
        # Nếu có trang riêng cho bank transfer, thì thay đổi đường dẫn và template
        return redirect('https://pay.vnpay.vn/Transaction/PaymentMethod.html?token=0208c031e98646c29e936b385c26dd88')
# QR Code 
def generate_qr(order_id,expiration_time_minutes=1):
    # Truy xuất thông tin từ cơ sở dữ liệu dựa trên order_id
    order = Order.query.get(order_id)

    if not order:
        return "Order not found", 404

    # Tính toán thời gian hiện tại và thời gian hết hạn
    
    current_time = datetime.utcnow()
    expiration_time = current_time + timedelta(minutes=expiration_time_minutes)

    # Tạo nội dung mã QR từ thông tin trong bảng Order
    qr_content = f"Order success!\nThank you {order.first_name} {order.last_name}\nOrders for ${order.total_price} will be delivered to you soon\nOrder tracking:\n'http:/127.0.0.1:5000/home'"

    # Tạo mã QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    # Tạo ảnh QR code bằng thư viện PIL
    img = qr.make_image(fill_color="black", back_color="white")

    # Lưu ảnh hoặc hiển thị
    if current_time <= expiration_time:
        img_path = os.path.abspath(f"qrcodes/order_{order.id}.png")
        img.save(img_path)

        # Hiển thị ảnh (có thể sử dụng send_file để hiển thị trực tiếp)
        response = make_response(send_file(img_path, mimetype='image/png'))

        # Ngăn chặn cache bằng cách thêm các header
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        return response
    else:
        return "QR Code has expired", 400

@views.route('/show_qr/<int:order_id>')
def show_qr(order_id):
    return generate_qr(order_id)
# Admin 
@views.route('/dashboard')
@views.route('/management_dashboard')
@login_required
def management_dashboard():
    return render_template('admin_dashboard.html')
@views.route('/management_month')
def management_month():
    orders = (
        db.session.query(Order)
        .with_entities(Order.id, Order.first_name, Order.last_name, Order.phone_number, Order.address,  Order.total_price)
        .all()
    )

    return render_template('admin_month.html', orders=orders)

# Route để xử lý sự kiện phê duyệt
@views.route('/approve_order/<int:order_id>')
def approve_order(order_id):
    # Xử lý logic phê duyệt ở đây (ví dụ: cập nhật trạng thái đơn hàng)
    return redirect(url_for('views.management_month'))

# Route để xử lý sự kiện từ chối
@views.route('/reject_order/<int:order_id>')
def reject_order(order_id):
    # Xử lý logic từ chối ở đây (ví dụ: cập nhật trạng thái đơn hàng)
    return redirect(url_for('views.management_month'))

# Route để xử lý sự kiện xóa khách hàng đặt hàng
@views.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    # Xử lý logic xóa ở đây
    order_to_delete = Order.query.get(order_id)
    db.session.delete(order_to_delete)
    db.session.commit()
    return redirect(url_for('views.management_month'))
@views.route('/management_add', methods=['GET', 'POST'])
def management_add():
    if request.method == 'POST':
        product_name = request.form['productName']
        quantity = request.form['quantity']
        price = request.form['price']
        image = request.files['image']

        # Kiểm tra xem tên sản phẩm đã tồn tại chưa
        existing_product = Amin_addProduct.query.filter_by(productName=product_name).first()

        if existing_product:
            flash("Product with the same name already exists in the database", category="error")
            return redirect(url_for('views.management_add'))

        new_product = Amin_addProduct(productName=product_name, quantity=quantity, price=price)

        # Lưu ảnh và cập nhật tên file trong cơ sở dữ liệu
        if image:
            image.save('E:/Mew/Code/PYTHON/FS_MANAGEMENT_WEBSITE/management/imgdatabase/{image.filename}')
            new_product.image = image.filename

        db.session.add(new_product)
        db.session.commit()
        flash("Add to success", category="success")

    products = Amin_addProduct.query.with_entities(Amin_addProduct.productName.label('productName')).all()
    return render_template('admin_add.html')
@views.route('/management_week')
def management_week():
    # Truy vấn tất cả các sản phẩm từ cơ sở dữ liệu
    all_products = Amin_addProduct.query.all()
    all_orders = Order.query.all()

    # Tính tổng số tiền
    total_price = sum(float(product.quantity) * float(product.price) for product in all_products)
    total_price_order = sum(order.total_price for order in all_orders)

    # Truyền giá trị total_price sang template admin_week.html
    return render_template('admin_week.html', total_price=total_price,total_price_order=total_price_order)
@views.route('/management_list')
def management_list():
    # Lấy danh sách các admin từ cơ sở dữ liệu
    products = Amin_addProduct.query.all()
    return render_template('admin_list.html', products=products)
# Xóa sản phẩm trong danh sách sản phẩm được quản lí 
@views.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    # Xử lý logic xóa ở đây
    product_to_delete = Amin_addProduct.query.get(product_id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('views.management_list'))
# Sửa thông tin sản phẩm
@views.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    # Tìm sản phẩm cần cập nhật từ cơ sở dữ liệu
    product = Amin_addProduct.query.get_or_404(product_id)

    # Cập nhật thông tin sản phẩm từ dữ liệu gửi từ phía client
    product.productName = request.json.get('productName', product.productName)
    product.price = request.json.get('price', product.price)
    product.quantity = request.json.get('quantity', product.quantity)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.session.commit()

    # Trả về thông báo cập nhật thành công (hoặc có thể trả về JSON khác tùy ý)
    return jsonify({'message': 'Product updated successfully'})
# Tìm kiếm sản phẩm
@views.route('/search_products', methods=['POST'])
def search_products():
    search_term = request.form.get('search_term', '')
    
    # Thực hiện truy vấn cơ sở dữ liệu để lấy danh sách sản phẩm thỏa mãn điều kiện tìm kiếm
    products = Amin_addProduct.query.filter(Amin_addProduct.productName.ilike(f'%{search_term}%')).all()

    return render_template('admin_list.html', products=products)