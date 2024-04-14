function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}
fetch(window.location.pathname + 'api/v1/', {
    headers: {
        ...includeAuthToken(),
        'Content-Type': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => {
        const { address_info } = data;

        document.getElementById('province').value = data.province;
        document.getElementById('city').value = data.city;
        document.getElementById('address-detail').value = data.detailed_address;
        document.getElementById('postal-code').value = data.postal_code;
        document.getElementById('profile-image').innerHTML = `<img src=${data.user.image} alt="profile_image" class="rounded-circle" width="150">
          <div class="mt-3">
            <h4>${data.user.first_name} ${data.user.last_name}</h4>
        </div>`;

    })
    .catch(error => console.error('Error fetching address data:', error));

function submitAddressForm() {
    const formData = {
        province: document.getElementById('province').value,
        city: document.getElementById('city').value,
        detailed_address: document.getElementById('address-detail').value,
        postal_code: document.getElementById('postal-code').value,
    };

    fetch(window.location.pathname + "api/v1/", {
        method: 'PUT',
        headers: {
            ...includeAuthToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
                console.log('Success:', data);
                alert('Form submitted successfully!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error submitting form!');
        });
}