document.addEventListener('DOMContentLoaded', () => {
    // Check if 'success' query parameter is present in the URL
    const urlParams = new URLSearchParams(window.location.search);
    console.log('URL Params:', urlParams.toString()); // Debugging line
    if (urlParams.get('success') === 'true') {
        alert('Movie updated successfully');
    }
});