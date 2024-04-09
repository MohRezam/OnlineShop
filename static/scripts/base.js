document.addEventListener("DOMContentLoaded", function () {
    var loginLink = document.getElementById('login-btn');
    var logoutLink = document.getElementById('logout-btn');
    var profileLink = document.getElementById('profile');

    if (localStorage.getItem('access_token')) {
        loginLink.style.display = 'none';
        logoutLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        logoutLink.style.display = 'none';
        profileLink.style.display = 'block';
        profileLink.style.display = 'none';

    }
});

function logoutFunc() {
    localStorage.removeItem("access_token");
    window.location.reload();
}