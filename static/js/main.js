var openBtn = document.getElementById("shop-nav-btn-open");
var closeBtn = document.getElementById("shop-nav-btn-close");
var navBar = document.getElementsByClassName("shop-main-nav-links");
var cartTotal = document.getElementById("cart-total");
var updateCartBtns = document.getElementsByClassName("update-cart");
var form = document.getElementById("form");
var paypalWrapper = document.getElementById("paypal-container");
var cartContent = document.getElementById("cart-contents");


openBtn.addEventListener("click", function () {
    navBar[0].style.left = "0";
})
closeBtn.addEventListener("click", function () {
    navBar[0].style.left = "-200px";
})

function logout () {
    window.location = logout_url;
}

function login () {
    window.location = login_url;
}

function getCartTotal () {
    var request = new XMLHttpRequest();
    request.open("GET", getCartTotalURL)
    request.onload = function () {
        cartTotal.textContent = request.responseText;
    }
    request.send()
}
window.setInterval(getCartTotal, 1000)

for (var btn of updateCartBtns) {
    btn.addEventListener("click", function () {
        var productID = this.dataset.product;
        var action = this.dataset.action;
        
        
        if (user !== "AnonymousUser") {
            updateCartItems(productID, action);	
        } else {
            window.location = login_url;
        }
    })
}

function updateCartItems (productID, action) {
    fetch(updateCartURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({"product_id": productID, "action": action})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        alert(error)
    })
}


form.addEventListener("submit", function (e) {
    e.preventDefault();
    paypalWrapper.style.display = "block";
    form.style.display = "none";
    
    var shippingInfo = {
        "country": form.country.value,
        "city": form.city.value,
        "address": form.address.value,
        "zipcode": form.zipcode.value,
        "tel": form.tel.value,
        "price": cart_price_total
    }
    
    paypal.Buttons({
        createOrder: (data, actions) => {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: cart_price_total
                    }
                }]
            });
        },
        onApprove: (data, actions) => {
            return actions.order.capture().then(function(orderData) {
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                const transaction = orderData.purchase_units[0].payments.captures[0];
                processOrder(shippingInfo)
            });
        }
    }).render('#paypal-button-container');

})

function processOrder (shippingInfo) {
    fetch(shippingURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({"address": shippingInfo.address, "city": shippingInfo.city, "country": shippingInfo.country, "zipcode": shippingInfo.zipcode, "tel": shippingInfo.tel, "cart_price_total": shippingInfo.price})
    })
    .then(response => response.json())
    .then(data => {
        alert(data);
        window.location = "{% url 'products:shop' %}";
    })
    .catch(error => {
        alert(error)
    })
}
