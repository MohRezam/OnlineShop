function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}

var data;
fetch('api/', {
    headers: {
        ...includeAuthToken(),
        'Content-Type': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => {
        console.log(data.calculate_total_price)
        document.getElementById('username').innerHTML = 'Thanks for your Order ' + data.serializer.user.first_name;
        document.getElementById('total-price').innerHTML = 'total price: ' + data.serializer.calculate_total_price;
        document.getElementById('created-at').innerHTML = 'created at ' + data.serializer.created_at;
        document.getElementById('Paid').innerHTML = 'is paid: ' + data.serializer.is_paid;
        document.getElementById('total-paid').innerHTML = data.serializer.calculate_total_price;
        data.address_data.forEach(address => {
            const option = document.createElement('option');
            option.value = address.id;
            option.text = `${address.province}, ${address.city}, ${address.detailed_address}`;
            document.getElementById('addressDropdown').appendChild(option);
        });
        this.data = data;
    })
    .catch(error => console.error('Error:', error));

document.getElementById('addressDropdown').addEventListener('change', function (event) {
    var selectedAddressId = this.value;
    if (selectedAddressId) {
        var selectedAddress = data.address_data.find(address => address.id === parseInt(selectedAddressId));
        document.getElementById('province').value = selectedAddress.province;
        document.getElementById('city').value = selectedAddress.city;
        document.getElementById('detail').value = selectedAddress.detailed_address;
        document.getElementById('post_code').value = selectedAddress.postal_code;

        document.getElementById('province').disabled = true;
        document.getElementById('city').disabled = true;
        document.getElementById('detail').disabled = true;
        document.getElementById('post_code').disabled = true;
    } else {
        document.getElementById('province').disabled = false;
        document.getElementById('city').disabled = false;
        document.getElementById('detail').disabled = false;
        document.getElementById('post_code').disabled = false;
    }
});

function submitFormData() {
    var province = document.getElementById('province').value;
    var city = document.getElementById('city').value;
    var detail = document.getElementById('detail').value;
    var post_code = document.getElementById('post_code').value;
    var coupon_code = document.getElementById('coupon_code').value;
    var selectedAddressId = document.getElementById('addressDropdown').value;

    fetch('api/', {
        method: 'POST',
        headers: {
            ...includeAuthToken(),
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            province: province,
            city: city,
            detailed_address: detail,
            postal_code: post_code,
            coupon_code: coupon_code,
            selected_address_id: selectedAddressId
        })
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error:', response.statusText);
            }
        })
        .then(data => {
            window.location.href = data.redirect_url;
        })
        .catch(error => {
            window.location.reload();
        });
}


function submitCoupon() {
    var coupon_code = document.getElementById('coupon_code').value;

    fetch('api/', {
        method: 'POST',
        headers: {
            ...includeAuthToken(),
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            code: coupon_code,
        })
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error:', response.statusText);
            }
        })
        .then(data => {
            window.location.href = data.redirect_url;
        })
        .catch(error => {
            window.location.reload();
        });
}

document.getElementById('payButton').addEventListener('click', function (event) {
    event.preventDefault();

    if (!validateForm()) {
        return;
    }

    submitFormData();
});

function validateForm() {
    var province = document.getElementById('province').value;
    var city = document.getElementById('city').value;
    var detail = document.getElementById('detail').value;
    var post_code = document.getElementById('post_code').value;

    if (province.trim() === '' || city.trim() === '' || detail.trim() === '' || post_code.trim() === '') {
        return false;
    }

    return true;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}