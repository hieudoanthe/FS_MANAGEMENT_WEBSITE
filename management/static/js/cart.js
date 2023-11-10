document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.addToCart');

    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            // Tìm thông tin sản phẩm liên quan đến nút được nhấn
            const productCard = button.closest('.product-item');
            const productName = productCard.querySelector('h6').textContent;
            const productPrice = productCard.querySelector('.d-flex h6').textContent;
            const productImage = productCard.querySelector('img').getAttribute("src");

            // Tạo một đối tượng sản phẩm
            const product = {
                name: productName,
                price: productPrice,
                image: productImage,
            };

            // Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
            if (isProductInCart(product)) {
                alert("The product is already in your cart");
            } else {
                // Lấy giỏ hàng từ Local Storage
                let cart = JSON.parse(localStorage.getItem("cart")) || [];

                // Thêm sản phẩm vào giỏ hàng
                cart.push(product);

                // Lưu lại giỏ hàng vào Local Storage
                localStorage.setItem("cart", JSON.stringify(cart));

                alert("The product has been added to cart");
            }
        });
    });
});

// Hàm kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
function isProductInCart(product) {
    // Lấy giỏ hàng từ Local Storage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // Kiểm tra xem sản phẩm có trong giỏ hàng hay không
    return cart.some(item => item.name === product.name && item.price === product.price);
}
   
// Xóa sản phẩm cart.html
document.addEventListener('DOMContentLoaded', function () {
        const deleteCartButtons = document.querySelectorAll('.deleteCart');
        deleteCartButtons.forEach(function (button) {
            button.addEventListener('click', function (event) {
                var cardDelete = button.closest('tr');
                var productID = cardDelete.id; // Lấy ID của sản phẩm cần xóa

                // Gọi hàm xóa sản phẩm và truyền vào ID
                removeProduct(productID);

                // Xóa sản phẩm trên giao diện
                cardDelete.remove();
            })
        })
    });

    // Hàm xóa sản phẩm từ giỏ hàng
    function removeProduct(productID) {
        // Lấy vị trí của sản phẩm trong giỏ hàng dựa trên ID
        const productIndex = parseInt(productID.split('-')[1]) - 1;

        // Lấy giỏ hàng từ Local Storage
        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        // Xóa sản phẩm khỏi giỏ hàng
        cart.splice(productIndex, 1);

        // Lưu lại giỏ hàng mới vào Local Storage
        localStorage.setItem("cart", JSON.stringify(cart));
    }

// Hàm hiển thị sản phẩm trong giỏ hàng
function displayCartItems() {
    const cartTable = document.querySelector("tbody.align-middle");
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        // Hiển thị thông báo nếu giỏ hàng rỗng
        cartTable.innerHTML = "<tr><td colspan='5'>Your cart is empty</td></tr>";
    } else {
        // Duyệt qua từng sản phẩm trong giỏ hàng và thêm chúng vào trang cart.html
        cart.forEach((product, index) => {
            const newRow = document.createElement("tr");
            newRow.id = `product-${index + 1}`;
            newRow.innerHTML = `
                <td style="text-align: left;" class="align-middle"><img src="${product.image}" alt="" style="width: 50px;"> ${product.name}</td>
                <td class="align-middle">${product.price}</td>
                <td class="align-middle">
                    <div class="input-group quantity mx-auto" style="width: 100px;">
                        <div class="input-group-btn">
                            <button class="btn btn-sm btn-primary btn-minus" onclick="decrementQuantity('product-${index + 1}')">
                                <i class="fa fa-minus"></i>
                            </button>
                        </div>
                        <input id="product-${index + 1}-quantity" type="text" class="form-control form-control-sm bg-secondary text-center" value="1">
                        <div class="input-group-btn">
                            <button class="btn btn-sm btn-primary btn-plus" onclick="incrementQuantity('product-${index + 1}')">
                                <i class="fa fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </td>
                <td class="align-middle" id="product-${index + 1}-total">${product.price}</td>
                <td class="align-middle"><button class="btn btn-sm btn-primary deleteCart"><i class="fa fa-times"></i></button></td>
            `;
            cartTable.appendChild(newRow);
            cartTotal()
        });
    }
}

// Gọi hàm hiển thị giỏ hàng khi trang cart.html được tải
displayCartItems();

// Tính tổng sản phẩm
function cartTotal() {
    var cartItem = document.querySelectorAll('tbody tr')
    var toTal = 0
    // console.log(cartItem.length);
    for (var i = 0; i < cartItem.length; i++){
        // console.log(i);
        var inputValue = cartItem[i].querySelector('input').value
        var productPrice = parseFloat(cartItem[i].querySelector('td:nth-child(4)').textContent.replace("$", ""));

        // console.log(inputValue);
        // console.log(productPrice);
        total = inputValue * productPrice;
        // console.log(total)
        toTal = toTal + total;
        // console.log(toTal)
    }
    cartTotalP = document.querySelector('.mt-2 h5:nth-child(2)')
    cartTotalP.innerHTML = toTal.toFixed(2);
    console.log(cartTotalP)
}

//

document.addEventListener('DOMContentLoaded', function () {
    const checkoutButton = document.querySelector('#checkoutButton');

    checkoutButton.addEventListener('click', function () {
        const confirmLogin = confirm("Vui lòng đăng nhập để tiếp tục.");
        
        // Nếu người dùng không đồng ý đăng nhập, không thực hiện hành động tiếp theo
        if (!confirmLogin) {
            return;
        }

        // Kiểm tra xem người dùng đã đăng nhập hay chưa
        if (!hasUserToken()) {
            // Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
            window.location.href = '/login';
            return;
        }

        // Lấy thông tin sản phẩm từ bảng giỏ hàng
        const cartRows = document.querySelectorAll('.align-middle tr');

        const cartData = {
            products: []
        };

        cartRows.forEach(row => {
            const productName = row.querySelector('td:first-child').textContent;
            const productPrice = parseFloat(row.querySelector('td:nth-child(2)').textContent.replace("$", ""));
            const productQuantity = parseInt(row.querySelector('td:nth-child(3) input').value);

            // Thêm thông tin sản phẩm vào mảng products
            cartData.products.push({
                name: productName,
                price: productPrice,
                quantity: productQuantity
            });
        });

        // Gửi yêu cầu POST đến route '/checkout' từ trình duyệt
        fetch('/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cartData)
        })
        .then(response => response.json())
        .then(data => {
            // Xử lý phản hồi từ server nếu cần
            console.log(data);
            // Chuyển hướng đến trang checkout.html sau khi đăng nhập thành công
            window.location.href = '/checkout.html';
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Xóa giỏ hàng từ Local Storage sau khi đã gửi lên server
        localStorage.removeItem("cart");
    });

    // Hàm kiểm tra xem có token người dùng hợp lệ hay không
    function hasUserToken() {
        const userToken = localStorage.getItem('userToken');

        // Kiểm tra xem có token và token hợp lệ hay không (thí dụ, kiểm tra hết hạn)
        return userToken !== null && isTokenValid(userToken);
    }

    // Hàm kiểm tra xem token có hợp lệ hay không
    function isTokenValid(token) {
        // Thực hiện kiểm tra logic để đảm bảo token hợp lệ
        // Ví dụ: kiểm tra hết hạn, chữ ký, v.v.
        // Trả về true nếu token hợp lệ, ngược lại trả về false
        // (Đây chỉ là một ví dụ giả định, bạn cần thay thế nó bằng cách phù hợp với cấu trúc xác thực của bạn)
        return true;
    }
});
