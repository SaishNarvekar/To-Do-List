var email = document.getElementById('email-field');
var username = document.getElementById('username-field');
var password = document.getElementById('password-field')
var form  = document.getElementsByTagName('form')[0];

username.addEventListener('input',function(event){
    console.log("Hello World");
},false);

password.addEventListener('input',function(event){
    console.log("Hello World");
},false);

form.addEventListener("submit", function (event) {
    event.preventDefault();
  }, false);