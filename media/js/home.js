var bg = document.getElementById('section1');
var path = "/static/images/";
var i = 1;
setInterval(changebg, 5000);
function changebg() {
    if (i == 1) {
        bg.style.backgroundImage = 'url("/static/images/bgimage7.jpg")';
        i = 2
    }
    else if (i == 2) {
        bg.style.backgroundImage = 'url("/static/images/bgimage2.jpg")';
        i = 3
    }
    else if (i == 3) {
        bg.style.backgroundImage = 'url("/static/images/bgimage3.jpg")';
        i = 4
    }
    else if (i == 4) {
        bg.style.backgroundImage = 'url("/static/images/bgimage4.jpg"';
        i = 5
    }
    else if (i == 5) {
        bg.style.backgroundImage = 'url("/static/images/bgimage5.jpg")';
        i = 6
    }
    else if (i == 6) {
        bg.style.backgroundImage = 'url("/static/images/bgimage11.jpg")';
        i = 1
    }
    else {
        bg.style.backgroundImage = 'url("/static/images/bgimage8.jpg")';
        i = 1;

    }
}
var manu = document.getElementById('manu');
function openmanu(){
    manu.style.visibility="visible";
}
function closemanu() {
    manu.style.visibility='hidden';
}

var img = document.getElementsByTagName('img');
img.classList.add("img-fluid");