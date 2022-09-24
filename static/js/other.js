// loader
var loader = document.getElementById('Preloader');
document.body.style.overflowY = "hidden";

window.addEventListener('load', loaded);
function loaded() {
    document.body.style.overflowY = "visible";
    loader.style.display = "none";
}
document.getElementById('manuIcon').classList.remove('nav-active');

window.onoffline = ()=>{
    console.log("offline");
    internetStatus.style.visibility = "visible";
    
    internetStatus.innerHTML = `
    <div class="alert alert-warning d-flex align-items-center " role="alert" >

    <i class="bi bi-wifi-off"> </i>
    &nbsp; 
    <div>
      Your Offline!
    </div>
    </div>
    `;

}

window.ononline = ()=>{
    internetStatus.innerHTML = `
    <div class="alert alert-info d-flex align-items-center " role="alert" >

    <i class="bi bi-wifi"> </i>
    &nbsp; 
    <div>
      Your Online Now!
    </div>

    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" style="position: absolute;
    right: 2vw;"></button>
    `;
}

