console.log('mobile portrait');

window.addEventListener('resize', ()=>{

    resize_link = document.getElementById('resize');
    resize_link.href = '/';
    resize_link.click();
});