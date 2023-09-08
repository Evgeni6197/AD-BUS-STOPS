document.addEventListener("DOMContentLoaded", ()=>{

    console.log('dashboard2');

    const layout_body = document.getElementById('layout_body');
    const device = layout_body.dataset.device;
    const payment_ver_btns = document.querySelectorAll('.payment_ver_btn');
    const place_remove_ver_btns = document.querySelectorAll('.place_remove_ver_btn');

    const dashboard_general_container = document.getElementById('dashboard_general_container');
    const dashboard_navbar_container = document.getElementById('dashboard_navbar_container');
    const dashboard_content_container = document.getElementById('dashboard_content_container');
    const part = dashboard_content_container.dataset.part;
    const payment_ver_container = document.getElementById('payment_ver_container');
    const show_order_id = document.getElementById('show_order_id');
    const show_order_sum = document.getElementById('show_order_sum');
    
    const form_input_order_id = document.getElementById('form_input_order_id');
    const form_input_order_sum = document.getElementById('form_input_order_sum');
    const payment_submit_btn = document.getElementById('payment_submit_btn');
    const payment_back_btn = document.getElementById('payment_back_btn');
    const form = document.getElementById('form');
    const spinner_container = document.getElementById('spinner_container');

    var  current_btn, order_id, order_sum;


    // removing  link sidebar
    if (device === 'mobile' && part != 'front'){
        dashboard_general_container.classList.remove('row');
        dashboard_navbar_container.classList.add('invisible');
        dashboard_content_container.classList.remove('col-8');
    }

    // payment verification
    payment_ver_btns.forEach((element)=>{
        element.addEventListener('click',primary_click);            
    });   
    payment_submit_btn.addEventListener('click',payment_form_submit);
    payment_back_btn.addEventListener('click',back_fnc);


    // placement  and removal verification 
    place_remove_ver_btns.forEach((element)=>{
        element.addEventListener('click',(event)=>{            
            place_remove_ver_btns.forEach((element)=>{
                element.disabled = true;
            });
            event.target.parentNode.submit();
            spinner_container.classList.remove('invisible');
        });
    });






    function disable_all_primary_btns(){
        payment_ver_btns.forEach((element)=>{
            element.disabled = true;
        });
    }

    function enable_all_primary_btns(){
        payment_ver_btns.forEach((element)=>{
            element.disabled = false;
        });
    }

    function primary_click(event){
        disable_all_primary_btns();
        current_btn = event.target; 
        order_id = current_btn.dataset.order_id;
        order_sum =  current_btn.dataset.order_sum;     
        show_order_id.innerHTML = order_id;
        show_order_sum.innerHTML = order_sum; 
        form_input_order_id.value = order_id;
        form_input_order_sum.value = order_sum; 
        payment_ver_container.classList.remove('invisible');        
    }

    function payment_form_submit(){
        payment_submit_btn.disabled = true;
        payment_back_btn.disabled = true;        
        spinner_container.classList.remove('invisible');
        payment_ver_container.classList.add('invisible');
        form.submit(); 
    }

    function back_fnc(){        
        enable_all_primary_btns();
        payment_ver_container.classList.add('invisible'); 
    }

});