var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js";
document.head.appendChild(script);
console.log('working');

script.onload = function () {
    tinymce.init({
        selector: "#id_body,#id_title,#id_slug,#id_packageInfo",
        height: 400,
        width: '100%',
        plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak ',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            ' code codesample table emoticons template paste help',
            'print preview powerpaste casechange importcss tinydrive searchreplace autolink autosave save directionality advcode visualblocks visualchars fullscreen image link media mediaembed template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists checklist wordcount tinymcespellchecker a11ychecker textpattern noneditable help formatpainter pageembed charmap mentions quickbars linkchecker emoticons advtable'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | link image | print preview media fullpage | ' +
            'forecolor backcolor emoticons | help',
        menu: {
            favs: { title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons' }
        },
        menubar: 'favs file edit view insert format tools table help',
        content_css: 'css/content.css'
    });
    
}