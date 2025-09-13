// Popups and notifications

document.addEventListener('DOMContentLoaded', function(){      
    showNotification("daily");
});

async function showNotification(type, content){
    const delay = ms => new Promise(res => setTimeout(res, ms));
    const popup = document.getElementById('popup');
    const header = document.getElementById('pop-up-header');
    const body = document.getElementById('pop-up-body');

    if (type == "daily"){
        header.innerHTML = "Daily Reminder";
        body.innerHTML = "Don't forget to fill out your daily entry!";
    }else if (type == "achievement"){
        header.innerHTML = "Achievement Unlocked! -- " + content.achievementName;
        body.innerHTML = content.achievementDescription;
    }
    await delay(3000);
    popup.style.marginBottom = "20px";
    popup.style.opacity = "1";
    await delay(5000);
    popup.style.marginBottom = "-200px";
    popup.style.opacity = "0";

    header.innerHTML = "Easiest Header on the Planet";
    body.innerHTML = "Do your daily journal!";
}  