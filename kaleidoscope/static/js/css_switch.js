// Switching between themes
document.addEventListener('DOMContentLoaded', function() {
  console.log("loaded")
  
  let theme = localStorage.getItem("theme");  
  document.body.classList.add(theme)
  const checkboxes = document.querySelectorAll('.reward-checkbox');

  checkboxes.forEach(function(checkbox) {
    theme = localStorage.getItem("theme");
    if (checkbox.id == theme){
      checkbox.setAttribute('checked','checked');
    }
    console.log("checkbox -- ", checkbox)
      checkbox.addEventListener('change', function() {
        console.log("elistner added -- ", checkbox)
          theme = localStorage.getItem("theme");
          if (this.checked) {
            let col = checkbox.getAttribute("id")
            switch(col){
              case "dark":
                document.body.classList.add(col);
                document.body.classList.remove("light");
                document.body.classList.remove("red");
                localStorage.setItem("theme",col);
                break;
              case "light":
                document.body.classList.remove("dark");
                document.body.classList.add("light");
                document.body.classList.remove("red");
                localStorage.setItem("theme",col);
                break;
              case "red":
                document.body.classList.remove("dark");
                document.body.classList.remove("light");
                document.body.classList.add("red");
                localStorage.setItem("theme","red");
                break;
            }
            
              // Uncheck all other checkboxes
              checkboxes.forEach(function(cb) {
                  if (cb !== checkbox) {
                      cb.checked = false;
                  }
              });
          } else {
            document.body.classList.remove("dark");
            document.body.classList.remove("light");
            document.body.classList.remove("red");
            document.body.classList.add("root");
            localStorage.setItem("theme","root");
          }
      });
  });
});