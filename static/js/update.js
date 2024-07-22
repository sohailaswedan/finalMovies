document.addEventListener('DOMContentLoaded', () => {
    // Check if 'success' query parameter is present in the URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
        alert('Movie updated successfully');
    }
});