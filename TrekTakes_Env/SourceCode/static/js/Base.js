// // pre loader
var loader = document.getElementById('Preloader');
document.body.style.overflowY = "hidden";
window.document.addEventListener('load',loaded());
function loaded() {
    document.body.style.overflowY = "visible";
    loader.style.display = "none";
}
document.getElementById('manuIcon').classList.remove('nav-active');



const app = (() => {
    let body;
    let menu;
    let menuItems;

    const init = () => {
        body = document.querySelector('body');
        menu = document.querySelector('#manuIcon');
        menuItems = document.querySelectorAll('.nav__list-item');
        navList = document.querySelectorAll('.nav__list');


        applyListeners();
    };

    const applyListeners = () => {
        menu.addEventListener('click', () => toggleClass(body, 'nav-active'));
    };

    const toggleClass = (element, stringClass) => {
        if (element.classList.contains(stringClass)) {
            element.classList.remove(stringClass);
            console.log('close');
        }
        else {
            element.classList.add(stringClass);
            if (navList[0].clientHeight >= window.screen.height - 150) {
                setTimeout(() => {
                    navList[0].style.height = '80vh';
                    navList[0].style.width = 'auto';
                    navList[0].style.overflowY = 'scroll';
                    console.log(navList[0].style.overflowY);
                }, 1200);
            }
            console.log('open', navList[0].clientHeight >= window.screen.height - 150);
        }

    };

    init();
})();



