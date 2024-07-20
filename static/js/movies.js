document.addEventListener('DOMContentLoaded', () => {
    const addLink = document.getElementById('addLink');
    const updateLink = document.getElementById('updateLink');
    const deleteLink = document.getElementById('deleteLink');

    const userRole = sessionStorage.getItem('userRole');
    if (userRole === 'admin') {
        addLink.classList.add('d-block');
        updateLink.classList.add('d-block');
        deleteLink.classList.add('d-block');
    } else {
        addLink.classList.add('d-none');
        updateLink.classList.add('d-none');
        deleteLink.classList.add('d-none');
    }
});
const userEmail = document.getElementById("email-displayed"); 
let localEmail = localStorage.getItem("email"); 
if (localEmail) {
    userEmail.textContent = "Welcome, " + localEmail; 
} else {
    userEmail.textContent = "No email found"; 
}