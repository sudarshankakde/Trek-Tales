var manu = document.getElementById('manu');
var navbar = document.getElementById('navbar');
var x = window.matchMedia("(max-width: 576px)");
function openmanu() {
    manu.style.visibility = "visible";
    if (x.matches) {
        document.body.style.overflowY = 'hidden';
    }
    else {
        document.body.style.overflowY = 'auto';
    }
}
function closemanu() {
    manu.style.visibility = 'hidden';
    if (x.matches) {
        document.body.style.overflowY = 'auto';
    }
    else {
        pass
    }
}

var img = document.getElementsByTagName('img');
img.classList.add("img-fluid");
