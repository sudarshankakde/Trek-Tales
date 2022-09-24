const app = (() => {
    let body;
    let menu;
    let menuItems;

    const init = () => {
        body = document.querySelector('body');
        menu = document.querySelector('#manuIcon');
        menuItems = document.querySelectorAll('.nav__list-item');
        navContainer = document.getElementsByClassName('nav');


        applyListeners();
    };

    const applyListeners = () => {
        menu.addEventListener('click', () => toggleClass(body, 'nav-active'));
    };

    const toggleClass = (element, stringClass) => {
        if (element.classList.contains(stringClass)) {
            element.classList.remove(stringClass);
            navContainer.style.visiblity="hidden";
            console.log('close');
        }
        else {
            element.classList.add(stringClass);
            navContainer.style.visiblity= "visible";
            console.log('open');
        }

    };

    init();
})();



