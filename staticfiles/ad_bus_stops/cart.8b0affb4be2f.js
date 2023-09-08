document.addEventListener('DOMContentLoaded', ()=>{

    console.log('cart');

    const content_container = document.getElementById('content_container');
    const message = content_container.dataset.message; 
    const success_mess_cont = document.getElementById('success_mess_cont');
    const checkout_btn = document.getElementById('checkout_btn');

    const back_btn = document.getElementById('back_btn');
    const back_link = document.getElementById('back_link');

    back_btn.addEventListener('click',()=>{
        back_link.click();
    });

    checkout_btn.addEventListener('click',()=>{
        success_mess_cont.classList.remove('invisible');
    });

    if(message !== 'reload'){
        content_container.classList.remove('invisible');
    }


});