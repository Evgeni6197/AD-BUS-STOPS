
console.log('mobile landscape'); 

var portrait;

window.addEventListener('resize', ()=>{

    //redirection works only if viewport orientaion changes
    portrait = window.innerWidth <  window.innerHeight;
    if (portrait){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
}); 