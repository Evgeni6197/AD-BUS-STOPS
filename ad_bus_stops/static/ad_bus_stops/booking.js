document.addEventListener('DOMContentLoaded', ()=>{

    console.log('booking919')
    // const and var -s
        const layout_body = document.getElementById('layout_body');
        const nav_wrap_container = document.getElementById('nav_wrap_container');
        const app_explorer_username = layout_body.dataset.app_explorer_username;
        const device = layout_body.dataset.device;

        var book_buttons = document.querySelectorAll('.book_button');
        const info_button = document.querySelectorAll('.info_button');
        const stops_page_message_container = document.getElementById('stops_page_message_container');
        const cart_button = document.getElementById('cart_button');
        const general_booking_container = document.getElementById('general_booking_container');

        const general_stops_container = document.getElementById('general_stops_container');
        const stops_id_paginated = general_stops_container.dataset.stops_id_paginated ;
        var quantity_in_cart =  parseInt( general_stops_container.dataset.quantity_in_cart);
        const slots_container = document.getElementById('slots_container');

        const general_cart_container = document.getElementById('general_cart_container');
        const book_address = document.getElementById('book_address');
        const book_price = document.getElementById('book_price');
        const overlap_text = document.getElementById('overlap_text');
        const reload_text = document.getElementById('reload_text');
        const try_again_text = document.getElementById('try_again_text');
        
        const checkbox_container1 = document.getElementById('checkbox_container1');
        const checkbox_container2 = document.getElementById('checkbox_container2');
        const submit_button = document.getElementById('submit_button');
        const return_button = document.getElementById('return_button');
        const booking_address_ul = document.getElementById('booking_address_ul');    
        const close_icon1 = document.getElementById('close_icon1');
        const close_icon2 = document.getElementById('close_icon2');
        const close_icon3 = document.getElementById('close_icon3');

        const checkbox_wrapping_container = document.getElementById('checkbox_wrapping_container');
        const spinner = document.getElementById('spinner');
        const spinner_container = document.getElementById('spinner_container');
        const book_warning_message = document.getElementById('book_warning_message');
        const book_warning_message_1 = document.getElementById('book_warning_message_1');
        const book_warning_message_2 = document.getElementById('book_warning_message_2');
        const cart_link = document.getElementById('cart_link');

        var vacant_months, stop_id, street, house, price,  month_arr, months_to_book_arr, months_to_book;
        var temp, count, valid_choice, portrait, target_container, l, h , current_book_button;
        var vacant_months_arr,  order_id, btn, where_to_place_info_btn;
        var stop_id_paginated, updated_VacantFrom;
    //
    close_icon1.addEventListener('click',()=>{
        book_warning_message_1.classList.add('invisible');
    });
    close_icon2.addEventListener('click',()=>{
        book_warning_message_2.classList.add('invisible');
    });
    close_icon3.addEventListener('click',()=>{
        stops_page_message_container.classList.add('invisible');
        overlap_text.classList.add('invisible');
        reload_text.classList.add('invisible');
        try_again_text.classList.add('invisible');
    });
    info_button.forEach((element)=>{
        element.addEventListener('click',()=>{
            show_message(overlap_text);
        });       
    });
    activate_book_buttons();  
    cart_button.addEventListener('click',()=>{

        if (quantity_in_cart){
            cart_link.click();
        }
        
    });
    return_button.addEventListener('click',()=>{
        
        checkbox_container1.innerHTML = '';
        checkbox_container2.innerHTML = '';
        general_stops_container.classList.remove('invisible');
        general_booking_container.classList.add('invisible');
        
    });


    function activate_book_buttons(){
        book_buttons.forEach((element)=>{
            element.addEventListener('click', book_button_click);
        }); 
    }
    function  book_button_click(event){

        stops_page_message_container.classList.add('invisible');

        // getting data for further usage
        collect_data(event);
        order_id = parseInt(cart_button.dataset.order_id);

        // Opened order case
        if (order_id){
            //current_book_button.removeEventListener('click', book_button_click);
            deactivate_book_buttons()
            show_main_spinner();
            months_to_book = '';
            fetch_opened_order(stop_id, months_to_book , price, order_id);

        // brand  new  order case
        } else {             
            show_booking_slots();              
            if (device === 'mobile'){
                set_parameters();
                window.addEventListener('resize', set_parameters);
            }

            // Clicking submit button
            submit_button.addEventListener('click', submit_checkbox);
            
            function submit_checkbox(){ 
                
                // warning mesage if anonymous_check
                if (app_explorer_username === 'anonymous_check'){
                    explorer_required_message();

                // fetch checkbox input date    
                } else { 
                    if (checkbox_input_is_valid()){   
                        submit_button.removeEventListener('click', submit_checkbox);
                        show_secondary_spinner();
                        fetch_new_order(stop_id, months_to_book , price, order_id);
                    }               
                }                
            }
        }    
    }
    function  book_btn_replacement_with_info_btn(result){
        where_to_place_info_btn = result.where_to_place_info_btn;
        if (where_to_place_info_btn){
            for (let stop_id_pagin of where_to_place_info_btn.split(',')){
                btn = document.getElementById('btn_'+stop_id_pagin);
                replace_book_by_info_btn(btn);
                btn.removeEventListener('click', book_button_click);
            }
        }
    }    
    function create_checkbox(month, target_container){

        const newCheckboxDiv = document.createElement("div");
        newCheckboxDiv.className = "form-check";
                
        const newCheckboxInput = document.createElement("input");
        newCheckboxInput.className = "form-check-input bg_nav_blue";
        newCheckboxInput.type = "checkbox";
        newCheckboxInput.value = "";
        newCheckboxInput.id = month;

        const newCheckboxLabel = document.createElement("label");
        newCheckboxLabel.className = "form-check-label";
        newCheckboxLabel.htmlFor = month;
        newCheckboxLabel.innerHTML = month.split('_')[0];

        newCheckboxDiv.appendChild(newCheckboxInput);
        newCheckboxDiv.appendChild(newCheckboxLabel);
        target_container.appendChild(newCheckboxDiv);
    }
    function checkbox_input_is_valid(){

        book_warning_message_1.classList.add('invisible');                    
        book_warning_message_2.classList.add('invisible');

        // record input  data into an array
        months_to_book_arr = []
        for (let month of vacant_months_arr){
            if (document.getElementById(month).checked){
                months_to_book_arr.push(month);
            }
        }

        // empty input
        if ( ! months_to_book_arr.length ){
            valid_choice = false;
            book_warning_message_1.classList.remove('invisible');

        // checking if the chosen months are consecutive    
        } else {                       
            count = 0;  months_to_book = ''; valid_choice = true;
            for (month of months_to_book_arr){
                months_to_book += month.split('_')[0] + ',';
                if (count === 0){
                    tmp = parseInt(month.split('_')[1]);
                } else {
                    if (parseInt(month.split('_')[1]) - tmp != 1){
                        valid_choice = false;
                        book_warning_message_2.classList.remove('invisible');
                        break;
                    } else {
                        tmp = parseInt(month.split('_')[1]);
                    }
                }
                count ++;                       
            }
        } 
        return valid_choice;
    }
    function collect_data(event){
        current_book_button = event.target;

        stop_id = current_book_button.dataset.stop_id;
        price = current_book_button.dataset.price ;
        street = current_book_button.dataset.street;
        house = current_book_button.dataset.house;
        vacant_months = current_book_button.dataset.vacant_months;
    }
    function deactivate_book_buttons(){
        book_buttons.forEach((element)=>{
            element.removeEventListener('click', book_button_click);
        }); 
    }
    function explorer_required_message(){
        submit_button.classList.add('invisible');
        book_warning_message.classList.remove('invisible');
        booking_address_ul.classList.add('invisible');
    }
    function fetch_opened_order(stop_id, months_to_book , price, order_id){

        fetch('/book',{
            'method'  : 'PUT',
            'body': JSON.stringify({
                        stop_id: stop_id,
                        months_to_book: months_to_book ,
                        price: price,
                        order_id: order_id,
                    })
        })
        .then(()=>{

            fetch('/book_confirm/'+`${stop_id}/${order_id}/${stops_id_paginated}`)
            .then(response => response.json())
            .then(result => {

                activate_book_buttons();
                //  db connection error 
                if (!result.db_successful_connections){
                    hide_main_spinner();
                    show_message(reload_text);
                    //current_book_button.addEventListener('click', book_button_click)
                } else { 

                    // success                   
                    if (result.successful_cart_addition){
                        quantity_in_cart = result.quantity_in_cart;                                                
                        update_cart_appearence();
                        hide_main_spinner();
                        
                    // cart addition failed
                    } else {                                                  
                        cart_addition_opportunity = result.cart_addition_opportunity;
                        actual_price = result.actual_price;
                         
                        // cart timeframe intersects occupied months
                        if (! cart_addition_opportunity){
                            current_book_button.removeEventListener('click', book_button_click)
                            replace_book_by_info_btn(current_book_button);                        
                        }
                        
                        document.getElementById('priceSpan_'+stop_id).innerHTML = actual_price; 
                        current_book_button.dataset.price = actual_price;                     
                        hide_main_spinner();
                        show_message(try_again_text);                        
                    }
                }
            })
            .catch(()=>{
                console.log('catch  in fetch_opened_order  fetch: GET') 
               hide_main_spinner();
               show_message(reload_text);
            })
        })
    }
    function fetch_new_order(stop_id, months_to_book , price, order_id){

        fetch('/book',{
            'method'  : 'PUT',
            'body': JSON.stringify({
                        stop_id: stop_id,
                        months_to_book: months_to_book ,
                        price: price,
                        order_id: order_id,
                    })
        })
        .then(()=>{

            fetch('/book_confirm/'+`${stop_id}/${order_id}/${stops_id_paginated}` )
            .then(response => response.json())
            .then(result => {
 
                //  db connection error 
                if (!result.db_successful_connections){
                    show_message(reload_text);
                    return_button.click();
                    
                } else {
                    
                    // success
                    if (result.order_created){
                        quantity_in_cart = result.quantity_in_cart;
                        current_book_button.removeEventListener('click', book_button_click);
                        update_cart_appearence();
                        cart_button.dataset.order_id = result.order_id;
                        book_btn_replacement_with_info_btn(result);

                        for ( let item of result.updated_paginated_VacantFrom_all.split(',')){
                            stop_id_paginated = item.split('_')[1];
                            updated_VacantFrom = item.split('_')[0];
                            update_VacantFrom_prompt(updated_VacantFrom,stop_id_paginated);
                        }
                        return_button.click();                        

                    // booking faluire    
                    } else {
                        actual_price = result.actual_price;
                        vacant_from = result.vacant_from;
                        
                        current_book_button.dataset.price = actual_price;
                        current_book_button.dataset.vacant_months = result.vacant_months;

                        document.getElementById('priceSpan_'+ stop_id).innerHTML = actual_price;
                        update_VacantFrom_prompt(vacant_from, stop_id  );                        
                        return_button.click();
                        show_message(try_again_text); 
                    }
                }
            })
            .catch(()=>{
                console.log('catch in fetch_new_order  ');
                show_message(reload_text);
                return_button.click();
            });
        })        
    }
    function hide_main_spinner(){
        stops_page_message_container.classList.add('invisible');
        spinner_container.classList.add('invisible');
        close_icon3.classList.remove('invisible');
    }
    function hide_secondary_spinner(){
        spinner.classList.add('invisible');
        booking_address_ul.classList.remove('invisible');
        submit_button.classList.remove('invisible');
    }
    function replace_book_by_info_btn(button){
        button.classList.remove("btn-outline-primary",'book_button');
        button.classList.add('btn-info','info_button');
        button.innerHTML = '&nbsp;&nbsp;Info&nbsp;&nbsp;&nbsp;';       
        button.addEventListener('click',()=>{
            show_message(overlap_text);        
        });
        book_buttons = document.querySelectorAll('.book_button');
    }
    function set_parameters(){
        h = nav_wrap_container.offsetHeight;
        checkbox_wrapping_container.style.height = `${(window.innerHeight-h)*0.85}px`
    }
    function show_booking_slots(){

        hide_secondary_spinner();
        general_stops_container.classList.add('invisible');
        general_booking_container.classList.remove('invisible');

        book_warning_message.classList.add('invisible');
        book_warning_message_1.classList.add('invisible');
        book_warning_message_2.classList.add('invisible');

        book_address.innerHTML = street + '&nbsp;' + house;
        book_price.innerHTML = price;
                    
        if (vacant_months){  
            slots_container.classList.add('row');    
            vacant_months_arr= vacant_months.split(',');             
            count = 0;  l = vacant_months_arr.length;
            for (let month of vacant_months_arr){
                if(count < l/2 ){
                    create_checkbox(month,checkbox_container1 );
                } else {
                    create_checkbox(month,checkbox_container2 );
                }                
                count ++;
            }
        } else {
            slots_container.classList.remove('row');
            checkbox_container1.innerHTML = '<h5> No vacant slots </h5>';
            submit_button.classList.add('invisible');
        }
    }
    function show_main_spinner(){
        stops_page_message_container.classList.remove('invisible');
        spinner_container.classList.remove('invisible');
        overlap_text.classList.add('invisible');
        reload_text.classList.add('invisible');
        try_again_text.classList.add('invisible');
        close_icon3.classList.add('invisible');
    }
    function show_message(text){

        overlap_text.classList.add('invisible');
        reload_text.classList.add('invisible');
        try_again_text.classList.add('invisible');
        stops_page_message_container.classList.remove('invisible');
        text.classList.remove('invisible');
    }
    function show_secondary_spinner(){
        spinner.classList.remove('invisible');
        booking_address_ul.classList.add('invisible');
        submit_button.classList.add('invisible');
    }
    function update_cart_appearence(){

        cart_button.innerHTML = `Cart&nbsp;(${quantity_in_cart})`
        current_book_button.classList.remove("btn-outline-primary",'book_button');
        current_book_button.classList.add('btn-secondary','nowrap');
        current_book_button.innerHTML = 'in Cart';
        current_book_button.removeEventListener('click', book_button_click)
        document.getElementById('date_container_' + stop_id).classList.add('transparent');
        book_buttons = document.querySelectorAll('.book_button');
    }
    function update_VacantFrom_prompt(vacant_from_parameter, stop_id_parameter ){
        if (!vacant_from_parameter){
            try {
                document.getElementById('vacant_from_prompt_'+ stop_id_parameter).innerHTML = '';
            }                                
            catch(error){
                // No such html element : device = 'desktop' case
                console.log('catch :  no vacant_from_prompt')
            }                                
        }
        document.getElementById('vacant_from_' + stop_id_parameter).innerHTML = vacant_from_parameter; 
    }

});