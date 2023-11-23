// Hàm xóa sản phẩm từ giỏ hàng và cơ sở dữ liệu
    function deleteProduct(productId) {
        const confirmDelete = confirm("Are you sure you want to remove this product from your cart?");

        if (confirmDelete) {
            // Gửi yêu cầu xóa sản phẩm từ cơ sở dữ liệu
            fetch(`/checkout/${productId}`, {
                method: 'DELETE',
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);

                    // Xóa sản phẩm khỏi giao diện
                    const productElement = document.getElementById(`product-${productId}`);
                    if (productElement) {
                        productElement.remove();
                         location.reload();
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        }
}
    

function submitForm() {
            // Lấy giá trị phương thức thanh toán được chọn
            const selectedPayment = document.querySelector('input[name="payment"]:checked');

            // Thêm giá trị phương thức thanh toán vào form
            const paymentInput = document.createElement('input');
            paymentInput.type = 'hidden';
            paymentInput.name = 'selected_payment';
            paymentInput.value = selectedPayment.value;

            document.getElementById('checkoutForm').appendChild(paymentInput);

            // Thực hiện lưu thông tin đơn hàng vào cơ sở dữ liệu
            document.getElementById('checkoutForm').submit();
        }