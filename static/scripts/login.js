document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("request");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        getToken();
    });

    function getToken() {
        const email = document.getElementById("email_input").value;
        const password = document.getElementById("password_input").value;

        fetch("http://127.0.0.1:80/auth/jwt/create/", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh_token", data.refresh);
                if (document.referrer == 'http://localhost/accounts/verify/') {
                    alert('You logged in successfully');
                    window.location.href = '/';
                } else {
                    alert('You logged in successfully');
                    window.location.href = document.referrer;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});