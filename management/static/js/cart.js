document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.addToCart');

    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            // Tìm thông tin sản phẩm liên quan đến nút được nhấn
            const productCard = button.closest('.product-item');
            const productName = productCard.querySelector('h6').textContent;
            const productPrice = productCard.querySelector('.d-flex h6').textContent;
            const productImage = productCard.querySelector('img').getAttribute("src");
            console.log(productPrice)
            // Tạo một đối tượng sản phẩm
            const product = {
                name: productName,
                price: parseFloat(productPrice.replace('$', '')), 
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
                // console.log(localStorage)
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
                cartTotal()
        const cartTable = document.querySelector("tbody.align-middle");
                let cart = JSON.parse(localStorage.getItem("cart")) || [];
                if (cart.length === 0) {
                // Hiển thị thông báo nếu giỏ hàng rỗng
                cartTable.innerHTML = "<tr><td colspan='5'>Your cart is empty</td></tr>";
                }
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
        // ... (Kiểm tra người dùng đã đăng nhập chưa)

        // Lấy thông tin sản phẩm từ Local Storage
        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        // Gửi thông tin sản phẩm lên máy chủ
        fetch('/save_checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ products: cart }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Chuyển hướng đến trang thanh toán sau khi lưu vào cơ sở dữ liệu
            // window.location.href = '/checkout';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
