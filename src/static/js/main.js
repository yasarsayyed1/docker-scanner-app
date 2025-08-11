// This file contains JavaScript code for the frontend, handling user interactions and making API calls to the backend.

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('image-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const imageName = document.getElementById('image-name').value;

        fetch('/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<h3>Scan Results:</h3><pre>${JSON.stringify(data.results, null, 2)}</pre>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });
});