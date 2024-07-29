function validateWordCount() {
    const maxWords = 100; // Set your maximum number of words here
    const description = document.getElementById('description').value;
    const wordCount = description.trim().split(/\s+/).length;

    if (wordCount > maxWords) {
        alert(`Maximum word limit of ${maxWords} words exceeded.`);
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}