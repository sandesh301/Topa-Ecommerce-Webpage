document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const changeQuantityBtns = document.querySelectorAll('.change-quantity');
    const deliveryChargeElement = document.getElementById("delivery-charge");

    changeQuantityBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const type = this.getAttribute('data-type');
            const cartItemId = this.getAttribute('data-cartitem');
            const quantitySpan = document.getElementById('quantity-' + cartItemId);
            const currentQuantity = parseInt(quantitySpan.innerText);

            let newQuantity;
            if (type === 'increase') {
                newQuantity = currentQuantity + 1;
            } else if (type === 'decrease') {
                newQuantity = Math.max(currentQuantity - 1, 1);
            }

            if (newQuantity >= 1) {
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/update_quantity/' + cartItemId + '/');
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        // Update the displayed quantity
                        quantitySpan.innerText = newQuantity;
                        updateTotalPrice(newQuantity, originalPrice, totalPriceElement);
                        updateSummaryTotal(cartItems, deliveryChargeElement); // Update summary on quantity change
                    }
                };
                const data = 'quantity=' + newQuantity;
                xhr.send(data);
            }
        });
    });

    const cartItems = document.querySelectorAll(".cart-item");

    cartItems.forEach(cartItem => {
        const quantityElement = cartItem.querySelector(".quantity");
        const priceElement = cartItem.querySelector(".product-price");
        const totalPriceElement = cartItem.querySelector(".total-price");
        const changeQuantityBtns = cartItem.querySelectorAll(".change-quantity");

        const originalPrice = parseFloat(priceElement.dataset.originalPrice);

        changeQuantityBtns.forEach(btn => {
            btn.addEventListener("click", function () {
                const type = btn.getAttribute("data-type");
                const currentQuantity = parseInt(quantityElement.innerText);

                const newQuantity = type === "increase" ? currentQuantity + 1 : Math.max(currentQuantity - 1, 1);

                quantityElement.innerText = newQuantity;
                updateTotalPrice(newQuantity, originalPrice, totalPriceElement);
                updateSummaryTotal(cartItems, deliveryChargeElement); // Update order summary on quantity change
            });
        });

        updateTotalPrice(parseInt(quantityElement.innerText), originalPrice, totalPriceElement);
    });

    function updateTotalPrice(quantity, originalPrice, totalPriceElement) {
        const total = (quantity * originalPrice).toFixed(2);
        totalPriceElement.innerText = "$" + total;
    }

    function updateSummaryTotal(cartItems, deliveryChargeElement) {
        let subtotal = 0;
        cartItems.forEach(cartItem => {
            const quantity = parseInt(cartItem.querySelector(".quantity").innerText);
            const originalPrice = parseFloat(cartItem.querySelector(".product-price").dataset.originalPrice);
            subtotal += quantity * originalPrice;
        });

        const subtotalElement = document.getElementById("subtotal");
        const totalElement = document.getElementById("total");

        const deliveryCharge = parseFloat(deliveryChargeElement.innerText);
        const total = subtotal + deliveryCharge;

        subtotalElement.innerText = subtotal.toFixed(2);
        totalElement.innerText = total.toFixed(2);
    }
});
