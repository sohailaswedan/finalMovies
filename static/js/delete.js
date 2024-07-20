function deleteMovie(movieId) {
    fetch(`/delete_movie/${movieId}`, {
        method: "GET",
    })
    .then()
   
}

// Delete account
const deleteAccount = document.getElementById("delete-account") ; 
deleteAccount.addEventListener("click", function() {
    fetch("/deleteAccount", { method: "POST" })
        .then(() => {
            // After deleting the account, redirect to the sign-up page
            window.location.href = "/signup"; 
        })
});





