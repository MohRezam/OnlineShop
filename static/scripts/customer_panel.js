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
        document.getElementById('first-name').textContent = data.customer_info.first_name;
        document.getElementById('last-name').textContent = data.customer_info.last_name;
        document.getElementById('phone-number').textContent = data.customer_info.phone_number;
        document.getElementById('user-email').textContent = data.customer_info.email;
        document.getElementById('profile-image').innerHTML = `<img src=${data.customer_info.image} alt="profile_image" class="rounded-circle" width="150">
          <div class="mt-3">
            <h4>${data.customer_info.first_name} ${data.customer_info.last_name}</h4>
          </div>`;
    })
    .catch(error => console.error('Error fetching user data:', error));

fetch(window.location.pathname + 'api/v1/', {
    headers: {
        ...includeAuthToken(),
        'Content-Type': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => {
        const addressTableBody = document.getElementById('address-table-body');

        data.address_info.forEach(function (address) {
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
              <td>${address.province}</td>
              <td>${address.city}</td>
              <td>${address.detailed_address}</td>
              <td>${address.postal_code}</td>
              <td>
                  <button class="btn btn-primary edit-address-btn" data-address-id="${address.id}">Edit</button>
              </td>
          `;
            addressTableBody.appendChild(newRow);

            const editBtn = newRow.querySelector('.edit-address-btn');
            editBtn.addEventListener('click', function () {
                const addressId = this.getAttribute('data-address-id');
                window.location.href = `/accounts/address/edit/${addressId}/`;
            });
        });
    })
    .catch(error => console.error('Error fetching address data:', error));