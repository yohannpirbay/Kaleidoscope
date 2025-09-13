document.addEventListener('DOMContentLoaded', function(){
    setupEntryCreation();
    setupCopyQuestionFeature();
    setupEntrySidebarManagement();
    setupImageUploading();
});

// Add event listener for the create entry button
function setupEntryCreation(){
    document.getElementById('new-entry-btn').addEventListener('click', function() {
        createNewEntry();
    });
}

// Setup the feature to select and delete entries from the sidebar
function setupEntrySidebarManagement(){
    document.querySelector('.entries').addEventListener('click', function(event){
        // Entry selection
        if(event.target.classList.contains('entry') || event.target.closest('.entry')){
            const entryId = event.target.closest('.entry').getAttribute('data-entry-id');
            loadEntryContent(entryId);
        }

        // Entry deletion
        if(event.target.closest('.delete-entry-btn')){
            const entryId = event.target.closest('.delete-entry-btn').getAttribute('data-entry-id');
            deleteEntry(entryId);
        }
    });
}

// Setup the clipboard feature for generated questions
function setupCopyQuestionFeature(){
    document.getElementById('copyQuestionBtn').addEventListener('click', function() {
        // Get the text from the element containing the question
        const questionText = document.getElementById('questionText').innerText;
        // Use the Clipboard API to copy the text
        navigator.clipboard.writeText(questionText).then(() => {
          const originalButtonText = this.innerText; // Save the original button text
          this.innerText = 'Copied!'; // Change button text to 'Copied!'
      
          // Set a timeout to revert the button text back to its original state after 2 seconds (2000 milliseconds)
          setTimeout(() => {
            this.innerText = originalButtonText;
          }, 2000); // Adjust time as needed
        }).catch(err => {
          console.error('Failed to copy text: ', err);
        });
    });  
}

// Setup the feature to upload images to the journal entry
function setupImageUploading(){
    document.getElementById('image-upload').addEventListener('change', function(event) {
        const file = event.target.files[0];

        // Ensure that the file is an image before proceeding
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgSrc = e.target.result;

                const imgElement = `<div class="uploaded-image-container">
                    <img src="${imgSrc}" onclick="showResizeIcon(this)" alt="Uploaded Image" class="uploaded-image"> 
                    <button class="btn btn-sm delete-image-btn text-red" onclick="deleteImage(event)"><i class="bi bi-x"></i></button>
                    <div class="resize-handle top-left" onmousedown="startResize(this, event)" onmouseup="stopResize()"></div>
                    <div class="resize-handle top-right" onmousedown="startResize(this, event)" onmouseup="stopResize()"></div>
                    <div class="resize-handle bottom-left" onmousedown="startResize(this, event)" onmouseup="stopResize()"></div>
                    <div class="resize-handle bottom-right" onmousedown="startResize(this, event)" onmouseup="stopResize()"></div>          
                  </div>`;

                // Append the image to the entry content
                const entryContent = document.querySelector('.entry-content');
                console.log(entryContent);
                entryContent.innerHTML += imgElement;

                // Log the contents of the uploaded-image-container
                const uploadedImageContainer = document.querySelector('.uploaded-image-container');
                console.log(uploadedImageContainer);
            };
            reader.readAsDataURL(file);
        } else {
            console.error('Invalid file format. Please select an image file.');
        }
    });
}

// Start resizing an image
function startResize(handle, event){
    isResizing = true;
    startX = event.clientX || event.touches[0].clientX;
    startY = event.clientY || event.touches[0].clientY;
    startWidth = parseInt(
        document.defaultView.getComputedStyle(handle.parentElement.querySelector('.uploaded-image')).width,
        10
    );
    startHeight = parseInt(
        document.defaultView.getComputedStyle(handle.parentElement.querySelector('.uploaded-image')).height,
        10
    );

    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);
    document.addEventListener('touchmove', resize); // For touch devices
    document.addEventListener('touchend', stopResize); // For touch devices
}

// Stop resizing an image
function stopResize(){
    isResizing = false; 
    document.removeEventListener('mousemove', resize);
}

// Resize images in the entry
function resize(event){
    if (!isResizing) return;
    const deltaX = event.clientX - startX;
    const deltaY = event.clientY - startY;
    const newWidth = startWidth + deltaX;
    const newHeight = startHeight + deltaY;
    const img = event.target.parentElement.querySelector('.uploaded-image');
    img.style.width = newWidth + 'px';
    img.style.height = newHeight + 'px';
}

// Show the resize icon for an image
function showResizeIcon(img) {
    const container = img.parentElement;
    const resizeHandles = container.querySelectorAll('.resize-handle');
    resizeHandles.forEach(handle => {
        if (handle.style.display === 'block') {
            handle.style.display = 'none';
        } else {
            handle.style.display = 'block';
        }
    });
}

// Initialisation for dragging an image in the entry
function initDrag(img, event){
    startX = event.clientX;
    startY = event.clientY;
    startLeft = parseInt(
        document.defaultView.getComputedStyle(img).left,
        10
    );
    startTop = parseInt(
        document.defaultView.getComputedStyle(img).top,
        10
    );

    document.addEventListener('mousemove', dragImage);
    document.addEventListener('mouseup', stopDrag);
}

// Stopping dragging an image in the entry
function stopDrag() {
    // Remove event listeners for mousemove and mouseup events
    document.removeEventListener('mousemove', dragImage);
    document.removeEventListener('mouseup', stopDrag);
}

// Drag an image in the entry
function dragImage(event){
    const deltaX = event.clientX - startX;
    const deltaY = event.clientY - startY;
    const newLeft = startLeft + deltaX;
    const newTop = startTop + deltaY;

    const img = event.target;
    img.style.left = newLeft + 'px';
    img.style.top = newTop + 'px';
}

// Show the dragging image indicator
function showMoveIndicator(img) {
    const container = img.parentElement;
    const moveIndicator = container.querySelector('.move-indicator');
    if (moveIndicator.style.display === 'block') {
        moveIndicator.style.display = 'none';
    } else {
        moveIndicator.style.display = 'block';
    }
}

// Deletion of an image n the entry
function deleteImage(event){
    const imageElement = event.target.closest('.uploaded-image-container');
    imageElement.remove();
}

// Save changes made to an entry
function saveEntry(entryId){
    const updatedText = document.querySelector('.entry-content').innerHTML;
    const updatedTitle = document.getElementById("entry-title-edit").innerText;
    
    // Get image sources from all uploaded images
    const images = document.querySelectorAll('.uploaded-image');
    const imageSources = [];
    images.forEach(image => {
        imageSources.push(image.src);
    });

    const csrftoken = getCookie('csrftoken');
    const moodTrackerContainer = document.getElementById('mood-value');
    const selectedMood = moodTrackerContainer.value;

    fetch(`/update_entry/${entryId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: updatedTitle,
            text: updatedText,
            mood: selectedMood,
            images: imageSources  // Include image sources in the payload
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            updateSideBar(updatedTitle,updatedText, entryId);
        }else{
            console.error("Failed to update entry", data.message);
        }
    })
    .catch(error => {
        console.error(error);
    });
}

// Set up the auto saving functionality
function autoSaveSetup(entryId){
    let timer;
    const interval = 2000;

    document.getElementById('entry-edit').addEventListener('input', () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            saveEntry(entryId);
        }, interval);
    });
}

// Download an entry as a PDF
function downloadEntry() {
    const updatedText = document.querySelector('.entry-content').innerHTML;
    const updatedTitle = document.querySelector('.entry-title').innerHTML;
    csrftoken = getCookie("csrftoken")

    console.log(updatedText);

    const dataToSend = {
        "entryTitle":updatedTitle,
        "entryText": updatedText 
    };

    fetch('/single_download/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
            // Add any other headers if needed
        },
        body: JSON.stringify(dataToSend),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.blob();  // Extract the response as a Blob
    })
    .then(blob => {
        // Create a download link and trigger the download
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'entry.pdf';  // Specify the filename
        link.click();
    })
    .catch(error => {
        // Handle errors during the request
        console.error('Error:', error);
    });
}

// Download multiple entries as PDFs
function multiplePDFDownloads(){
        let selectedEntries = document.querySelectorAll('.entry-checkbox:checked');
        if (selectedEntries.length === 0) {
            alert('Please select an entry.');
            return;
        }
        csrftoken = getCookie("csrftoken")
        
        let selectedEntryIDs = []
        selectedEntries.forEach(function(checkbox) {
            let entryText = checkbox.parentElement.getAttribute("archive_entry_id").trim();
            selectedEntryIDs.push(entryText);
        });
        dataToSend = {"entries":selectedEntryIDs}

        fetch('/multiple_download/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
                // Add any other headers if needed
            },
            body: JSON.stringify(dataToSend),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.blob();  // Extract the response as a Blob
        })
        .then(blob => {
            // Create a download link and trigger the download
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'entries.zip';  // Specify the filename
            link.click();
        })
        .catch(error => {
            // Handle errors during the request
            console.error('Error:', error);
        });
        
    };

// Change the URL to email
function goToEmail() {
    window.location.href = 'email/';
}

// Generate the inspiration question from a given prompt
function generateInspiringQuestion() {
    let userInput = document.getElementById('userInput').value;

    // Ensure the input is not empty
    if (userInput.trim() !== '') {
        fetch('/generate_inspiring_question/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({user_input: userInput})
        })
        .then(response => response.json())
        .then(data => {
            displayQuestionModal(data.question); // Function to display the question in a modal
        })
        .catch(error => console.error('Error:', error));
    } else {
        // Handle empty input case
        alert('Please enter something about your day!');
    }
}

// Function to display the question in a modal
function displayQuestionModal(question) {
    let modalBody = document.getElementById('questionText');
    modalBody.innerText = question;

    // Code to display the modal, depends on how your modal is implemented
    // If using Bootstrap, you might need something like this:
    // let questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
    // questionModal.show();

    // Alternatively, you can use jQuery if it's included in your project:
    $('#questionModal').modal('show');
}

// Deletion of reminders
function deleteReminder(reminder_id){
    const data = JSON.stringify({ id: reminder_id });
    fetch('/delete_reminder/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: data
    })
}

// Travel 1 page back
function goBack() {
    window.history.back();
}