const username = document.getElementById("username-displayed"); 
let localUsername = localStorage.getItem("userName"); 
if (localUsername) {
    username.textContent = "Welcome " + localUsername; 
} else {
    username.textContent = "No email found"; 
}