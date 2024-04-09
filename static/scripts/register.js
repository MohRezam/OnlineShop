document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    // Call the registerFunc() function to handle form submission
    registerFunc();
});

function registerFunc() {
    var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;
    var phone_number = document.getElementById("phone_number").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    fetch("/accounts/register/api/v1/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            first_name: first_name,
            last_name: last_name,
            phone_number: phone_number,
            email: email,
            password: password,
        })
    })
        .then(data => {
            alert('We sent to your email an OTP code');
            window.location.href = '/accounts/verify/';
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error);
            window.location.reload();
        });
}