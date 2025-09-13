// Info button for the app
document.addEventListener('DOMContentLoaded', function(){
    setupInfoBoxFeature();
});

function setupInfoBoxFeature(){
    const infoButton = document.getElementById('info-button');
    const closeButton = document.getElementById('close-button');
    const overlay = document.getElementById('overlay');
    const infoBox = document.getElementById('info-box');

    infoButton.addEventListener('click', function(){
        openInfoBox(infoBox, overlay);
    });

    closeButton.addEventListener('click', function(){
        closeInfoBox(infoBox, overlay);
    });
}

 // Open the info box
 function openInfoBox(infoBox, overlay){
     if (infoBox == null) return
     infoBox.classList.add('active');
     overlay.classList.add('active');
 }

 // Close the info box
 function closeInfoBox(infoBox, overlay){
     if (infoBox == null) return
     infoBox.classList.remove('active');
     overlay.classList.remove('active');
 }