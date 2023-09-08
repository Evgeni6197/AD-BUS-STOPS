console.log('mobile portrait');


var landscape;

window.addEventListener('resize', ()=>{

    //redirection works only if viewport orientaion changes
    landscape = window.innerWidth >  window.innerHeight;
    if (landscape){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
}); 