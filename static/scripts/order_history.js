function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}
document.addEventListener('DOMContentLoaded', function () {
    fetch('/accounts/api/order_history', {
        headers: {
            ...includeAuthToken(),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            data.queryset.forEach(item => {
                let row = document.createElement('tr');
                row.innerHTML = '<td>' + item.user.first_name + ' ' + item.user.last_name + '</td>' +
                    '<td>' + item.id + '</td>' +
                    '<td>' + item.calculate_total_price + '</td>' +
                    '<td>' + item.is_paid + '</td>' +
                    '<td><a href="/orders/detail/' + item.id + '" class="btn btn-primary">Checkout</a></td>';
                document.getElementById('cart-items').appendChild(row);
            });
        });
});