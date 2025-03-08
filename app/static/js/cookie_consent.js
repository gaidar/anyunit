
/* Cookied consent */

document.addEventListener('DOMContentLoaded', function () {
    const cookieConsent = document.getElementById('cookieConsent');
    const acceptCookies = document.getElementById('acceptCookies');

    // Check if consent has already been given
    if (!getCookie('cookie_consent')) {
        cookieConsent.style.display = 'block'; // Show the popup
    }

    // When the user clicks "Accept"
    acceptCookies.addEventListener('click', function () {
        setCookie('cookie_consent', 'accepted', 365);
        cookieConsent.style.display = 'none'; // Hide the popup
    });

    // Function to set a cookie
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    // Function to get a cookie
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
});
