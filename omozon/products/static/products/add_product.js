document.getElementById('add-image-button').addEventListener('click', function() {
    const imageContainer = document.getElementById('image-container');
    const newInput = document.createElement('input');
    newInput.type = 'file';
    newInput.name = 'images';
    newInput.accept = 'image/*';
    newInput.className = 'image-input';
    
    // Create a delete button for the new input
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.textContent = 'Remove';
    deleteButton.className = 'btn btn-danger remove-image-button';
    
    // Append the new input and delete button to the container
    imageContainer.appendChild(newInput);
    imageContainer.appendChild(deleteButton);
    
    // Add event listener to the delete button
    deleteButton.addEventListener('click', function() {
        imageContainer.removeChild(newInput);
        imageContainer.removeChild(deleteButton);
    });
}); 