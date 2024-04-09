function includeAuthToken() {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
        return {
            'Authorization': 'JWT ' + access_token
        };
    }
    return {};
}

fetch('/accounts/panel/api/v1/', {
    headers: {
        ...includeAuthToken(),
        'Content-Type': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => {
        const { customer_info, address_info } = data;

        document.getElementById('first-name').value = customer_info.first_name;
        document.getElementById('last-name').value = customer_info.last_name;
        document.getElementById('phone-number').value = customer_info.phone_number;
        document.getElementById('user-email').value = customer_info.email;
        document.getElementById('profile-image').innerHTML = `<img src=${customer_info.image} alt="profile_image" class="rounded-circle" width="150">
              <div class="mt-3">
                  <h4>${customer_info.first_name} ${customer_info.last_name}</h4>
              </div>`;


    })
    .catch(error => console.error('Error fetching user data:', error));

function submitForm() {
    const formData = {
        first_name: document.getElementById('first-name').value,
        last_name: document.getElementById('last-name').value,
        phone_number: document.getElementById('phone-number').value,
        email: document.getElementById('user-email').value,
    };

    fetch("/accounts/panel/api/v1/", {
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