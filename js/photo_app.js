const hamburgerToggle = (toggle) => {
  const hamburger = document.getElementById('hamburger');
  const hamburgerClose = document.getElementById('hamburgerClose');
  const navbarContainer = document.getElementById('navbarContainer');
  if (toggle === 1) {
    hamburger.style.display = "none";
    hamburgerClose.style.display = "block";
    navbarContainer.style.display = "flex";
  } else {
    hamburger.style.display = "flex";
    hamburgerClose.style.display = "none";
    navbarContainer.style.display = "none";
  }
};

const activateHotKeys = () => {
  document.addEventListener('keydown', function(event){
    if (event.keyCode === 39) {
      document.getElementById("nextPhoto").click();
    } else if (event.keyCode === 37) {
      document.getElementById("previousPhoto").click();
    }
    console.log(event.keyCode);
  });
};
