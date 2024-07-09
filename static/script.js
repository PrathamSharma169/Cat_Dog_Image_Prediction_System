function previewImage() {
    const imageInput = document.getElementById('imageInput');
    const file = imageInput.files[0];
    const preview = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        preview.src = '';
        preview.style.display = 'none';
    }
}

async function classifyImage() {
    const imageInput = document.getElementById('imageInput');
    const file = imageInput.files[0];

    if (!file) {
        alert("Please select an image first.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    console.log("Sending request to classify image");  // Debugging line

    try {
        const response = await fetch('http://127.0.0.1:5000/classify', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        console.log("Received response:", result);  // Debugging line

        const resultDiv = document.getElementById('result');
        if (result.success) {
            resultDiv.innerText = `The image is classified as: ${result.label}`;
        } else {
            resultDiv.innerText = 'Error: ' + result.message;
        }

        // Set a timeout to clear the result after 10 seconds
        setTimeout(() => {
            resultDiv.innerText = '';
        }, 10000);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred. Please try again.';
        
        // Set a timeout to clear the error message after 10 seconds
        setTimeout(() => {
            document.getElementById('result').innerText = '';
        }, 10000);
    }
}
