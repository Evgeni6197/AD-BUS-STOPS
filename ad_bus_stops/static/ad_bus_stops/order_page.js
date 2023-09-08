document.addEventListener('DOMContentLoaded', ()=>{

    console.log('order_page')

    const heading_wrap = document.getElementById('heading_wrap');
    const action = heading_wrap.dataset.action;
    const cancel_order_btn = document.getElementById('cancel_order_btn');

    const first = document.getElementById('first');
    const second = document.getElementById('second');
    const third = document.getElementById('third');
   
    if (action === 'cancel'){
        heading_wrap.classList.add('row');
        first.classList.remove('invisible');
        second.classList.add('col-8');
        third.classList.remove('invisible');
    }

    cancel_order_btn.addEventListener("click",(event)=>{
        cancel_order_btn.disabled = true;
        event.target.parentNode.submit();
    });
});