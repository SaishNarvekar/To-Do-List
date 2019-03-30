var email = document.getElementById('email-field');
var username = document.getElementById('username-field');
var password = document.getElementById('password-field')
var form = document.getElementsByTagName('form')[0];

var email_error = document.getElementById('email-error');
var username_error = document.getElementById('username-error');
var password_error = document.getElementById('password-error');

email.addEventListener('input', function (event) {
    console.log(email.value);
    if (email.value == "" || email.value == null) {
        email_error.style.display = "block";
        email_error.style.width = "300px";
        email_error.style.margin = "auto";
    }
    else{
        email_error.style.display = "none";
    }
}, false);

username.addEventListener('input', function (event) {
    // console.log(username.value);
    var result = /^[A-Za-z_0-9]{6,15}$/.test(username.value);
    if(!result){
        username_error.style.display = "block";
        username_error.style.width = "300px";
        username_error.style.margin = "auto";
    }
    else{
        username_error.style.display = "none";
    }
}, false);

password.addEventListener('input', function (event) {
    console.log(password.value);
}, false);

form.addEventListener("submit", function (event) {
    event.preventDefault();
}, false);

// username_error.style.display = "block";
// username_error.style.width = "300px";
// username_error.style.margin = "auto";