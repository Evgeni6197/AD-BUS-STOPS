document.addEventListener('DOMContentLoaded', ()=>{

    console.log('cart');

    const content_container = document.getElementById('content_container');
    const message = content_container.dataset.message; 

    const back_btn = document.getElementById('back_btn');
    const back_link = document.getElementById('back_link');

    back_btn.addEventListener('click',()=>{
        back_link.click();
    });

    if (message !== 'reload'){
        content_container.classList.remove('invisible');
    }



});