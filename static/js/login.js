var username = document.getElementById('username');
var password = document.getElementById('password')
var form  = document.getElementsByTagName('form')[0];
var username_error = document.getElementById('username-error');


username.addEventListener('input',function(event){
    username_error.style.display = "block";
    username_error.style.width = "300px";
    username_error.style.margin = "auto";
    console.log("Hello World");
},false);

password.addEventListener('input',function(event){
    console.log("Hello World");
},false);

form.addEventListener("submit", function (event) {
    console.log("yes")
    event.preventDefault();
  }, false);