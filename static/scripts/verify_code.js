document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault();
    verifyFunc();
});

function verifyFunc() {
    var code = document.getElementById('code').value;

    fetch("/accounts/verify/api/v1/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: code
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to verify code');
            }
            return response.json();
        })
        .then(data => {
            if (data.message) {
                alert(data.message);
            }

            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        })
        .catch(error => {
            alert("Error occurred: " + error.message);
        });
}

let timerOn = true;

function timer(remaining) {
    var m = Math.floor(remaining / 60);
    var s = remaining % 60;

    m = m < 10 ? '0' + m : m;
    s = s < 10 ? '0' + s : s;
    document.getElementById('timer').innerHTML = m + ':' + s;
    remaining -= 1;

    if (remaining >= 0 && timerOn) {
        setTimeout(function () {
            timer(remaining);
        }, 1000);
        return;
    }

    if (!timerOn) {
        return;
    }

    alert('Timeout for OTP');
    window.location.href = '/accounts/register/';
}

timer(180); 