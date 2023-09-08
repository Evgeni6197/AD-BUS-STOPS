document.addEventListener('DOMContentLoaded', ()=>{

    console.log('cart'); 

    const content_container = document.getElementById('content_container');
    const message = content_container.dataset.message; 
    const success_mess_cont = document.getElementById('success_mess_cont');
    const checkout_btn = document.getElementById('checkout_btn');
    const cancel_forms = document.querySelectorAll('.cancel_form');
    const  cancel_btns =  document.querySelectorAll('.cancel_btn');

    const back_btn = document.getElementById('back_btn');
    const back_link = document.getElementById('back_link');

    cancel_forms.forEach((element)=>{
        element.addEventListener('submit', (event)=>{
            event.preventDefault();
        })
    });

    cancel_btns.forEach((element)=>{
        element.addEventListener('click', submit_form); 
      
    });


    back_btn.addEventListener('click',()=>{
        back_link.click();
    });

    checkout_btn.addEventListener('click',()=>{
        success_mess_cont.classList.remove('invisible');
    });

    if(message !== 'reload'){
        content_container.classList.remove('invisible');
    }

    function submit_form(event){

        cancel_btns.forEach((element)=>{
            element.removeEventListener('click', submit_form); 
          
        });

        event.target.parentNode.submit();
    }
});