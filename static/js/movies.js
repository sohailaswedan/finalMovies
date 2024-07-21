const userEmail = document.getElementById("email-displayed"); 
let localEmail = localStorage.getItem("email"); 
if (localEmail) {
    userEmail.textContent = "Welcome, " + localEmail; 
} else {
    userEmail.textContent = "No email found"; 
}