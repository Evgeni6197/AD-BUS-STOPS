document.addEventListener('DOMContentLoaded', ()=>{

    console.log('cart1'); 

    const content_container = document.getElementById('content_container');
    const message = content_container.dataset.message; 
    const success_mess_cont = document.getElementById('success_mess_cont');
    const checkout_btn = document.getElementById('checkout_btn');
    const cancel_forms = document.querySelectorAll('.cancel_form');
    const  cancel_btns =  document.querySelectorAll('.cancel_btn');

    const back_btn = document.getElementById('back_btn');
    const back_link = document.getElementById('back_link');
    const checkout_form = document.getElementById('checkout_form');


    checkout_form.addEventListener('submit', ()=>{
        checkout_btn.disabled = true;
        back_btn.disabled = true;
        back_btn.removeEventListener('click', back_link_click);
        cancel_btns.forEach((element)=>{
            element.disabled = true;                   
        });
        success_mess_cont.classList.remove('invisible');
    })

    cancel_forms.forEach((element)=>{
        element.addEventListener('submit', (event)=>{
            event.preventDefault();
        })
    });

    cancel_btns.forEach((element)=>{
        element.addEventListener('click', submit_cancel_form);       
    });

    back_btn.addEventListener('click', back_link_click);

 

    if(message !== 'reload'){
        content_container.classList.remove('invisible');
    }

    function submit_cancel_form(event){
        cancel_btns.forEach((element)=>{
            element.removeEventListener('click', submit_cancel_form);           
        });
        event.target.parentNode.submit();
    }

    function back_link_click(){
        back_link.click();
    }

});