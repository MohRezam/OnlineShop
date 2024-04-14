function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}

function submitAddressForm() {
    const formData = {
        province: document.getElementById('province').value,
        city: document.getElementById('city').value,
        detailed_address: document.getElementById('address-detail').value,
        postal_code: document.getElementById('postal-code').value,
    };

    fetch(window.location.pathname + "api/v1/", {
        method: 'POST',
        headers: {
            ...includeAuthToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
        .then(data => {
            alert('Address added successfully')
            window.location.href = '/accounts/panel/';

        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error submitting form!');
        });
}