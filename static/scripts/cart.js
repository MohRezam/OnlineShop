function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}
function fetchCartData() {
    $.getJSON('/orders/api/cart/slug2', function (data) {
        $('#cartBody').empty();

        $.each(data.data, function (index, item) {
            $('#cartBody').append(
                `<tr>
                     <th scope="row">${index + 1}</th>
                     <td>${item.product.name}</td>
                     <td>${item.quantity}</td>
                     <td>${item.product.price}</td>
                     <td>${item.total_price}</td>
                     <td><a href="#" class="remove-link" data-slug="${item.product.slug}">Remove</a></td>
                 </tr>`
            );
        });

        $('#totalPrice').text(data.cart_total_price);

        var currentUrl = window.location.href;

        $('.remove-link').click(function (event) {
            event.preventDefault();
            var productSlug = $(this).data('slug');
            removeFromCart(productSlug, currentUrl);
        });
    });
}

function removeFromCart(productSlug, currentUrl) {
    $.getJSON(`/orders/cart/remove/${productSlug}`, function (data) {
        fetchCartData();
        window.location.href = currentUrl;
    });
}
$(document).ready(function () {
    fetchCartData();
});

$(document).on("click", "#checkoutButton", function (event) {
    event.preventDefault();

    fetch('/orders/cart/create/', {
        headers: {
            ...includeAuthToken(),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        })
        .catch(error => console.error('Error:', error));
});
document.addEventListener("DOMContentLoaded", function () {
    var loginLink = document.getElementById('login-btn');
    var logoutLink = document.getElementById('logout-btn');

    if (localStorage.getItem('access_token')) {
        loginLink.style.display = 'none';
        logoutLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        logoutLink.style.display = 'none';
    }
});

function logoutFunc() {
    localStorage.removeItem("access_token");
    window.location.reload();
}