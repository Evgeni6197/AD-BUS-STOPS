document.addEventListener('DOMContentLoaded', ()=>{

    console.log('booking3')
    const layout_body = document.getElementById('layout_body');
    const nav_wrap_container = document.getElementById('nav_wrap_container');
    const app_explorer_username = layout_body.dataset.app_explorer_username;
    const device = layout_body.dataset.device;

    const book_buttons = document.querySelectorAll('.book_button');
    const info_button = document.querySelectorAll('.info_button');
    const stops_page_message_container = document.getElementById('stops_page_message_container');
    const cart_button = document.getElementById('cart_button');
    const general_booking_container = document.getElementById('general_booking_container');
    const general_stops_container = document.getElementById('general_stops_container');
    const stops_id_paginated = general_stops_container.dataset.stops_id_paginated ;
    var quantity_in_cart =  parseInt( general_stops_container.dataset.quantity_in_cart);

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

    const order_id = parseInt(cart_button.dataset.order_id);
    const checkbox_wrapping_container = document.getElementById('checkbox_wrapping_container');
    const spinner = document.getElementById('spinner');
    const spinner_container = document.getElementById('spinner_container');
    const book_warning_message = document.getElementById('book_warning_message');
    const book_warning_message_1 = document.getElementById('book_warning_message_1');
    const book_warning_message_2 = document.getElementById('book_warning_message_2');

    var vacant_months, stop_id, street, house, price,  month_arr, months_to_book_arr, months_to_book;
    var temp, count, valid_choice, portrait, target_container, l, h , current_book_button;

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
        //spinner_container.classList.add('invisible');
    });

    info_button.forEach((element)=>{
        element.addEventListener('click',()=>{
            // stops_page_message_container.classList.remove('invisible');
            // overlap_text.classList.remove('invisible');
            show_message(overlap_text);
        });       
    });

    book_buttons.forEach((element)=>{
        element.addEventListener('click', book_button_click);
    });
   

    cart_button.addEventListener('click',()=>{
        general_stops_container.classList.add('invisible');
        general_cart_container.classList.remove('invisible');
    });

    return_button.addEventListener('click',()=>{
        
        checkbox_container1.innerHTML = '';
        checkbox_container2.innerHTML = '';
        general_stops_container.classList.remove('invisible');
        general_booking_container.classList.add('invisible');
        
    });



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

    function set_parameters(){
        h = nav_wrap_container.offsetHeight;
        checkbox_wrapping_container.style.height = `${(window.innerHeight-h)*0.85}px`
    }
    
    function hide_spinner(){
        stops_page_message_container.classList.add('invisible');
        spinner_container.classList.add('invisible');
        close_icon3.classList.remove('invisible');
    }

    function show_message(text){
        overlap_text.classList.add('invisible');
        reload_text.classList.add('invisible');
        try_again_text.classList.add('invisible');
        stops_page_message_container.classList.remove('invisible');
        text.classList.remove('invisible');
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

            fetch('/book_confirm/'+`${stop_id}/${order_id}/${stops_id_paginated}` )
            .then(response => response.json())
            .then(result => {

                //  db connection error 
                if (!result.db_successful_connections){
                    hide_spinner();
                    show_message(reload_text);
                    current_book_button.addEventListener('click', book_button_click)
                } else { 

                    // success                   
                    if (result.successful_cart_addition){
                        quantity_in_cart ++;
                        cart_button.innerHTML = `Cart&nbsp;(${quantity_in_cart})`
                        current_book_button.classList.remove("btn-outline-primary",'book_button');
                        current_book_button.classList.add('btn-secondary','nowrap');
                        current_book_button.innerHTML = 'in Cart';
                        document.getElementById('date_container_' + stop_id).classList.add('transparent');
                        hide_spinner();

                    // cart addition failed
                    } else {                
                        cart_addition_opportunity = result.cart_addition_opportunity
                        actual_price = result.actual_price
                        console.log('cart_addition_opportunity =',cart_addition_opportunity,actual_price )
                                              
                        if (! cart_addition_opportunity){
                            current_book_button.classList.remove("btn-outline-primary",'book_button');
                            current_book_button.classList.add('btn-info','info_button');
                            current_book_button.innerHTML = '&nbsp;&nbsp;Info&nbsp;&nbsp;&nbsp;';
                            current_book_button.addEventListener('click',()=>{
                                show_message(overlap_text);
                            });
                                        
                        } else {
                            current_book_button.addEventListener('click', book_button_click)
                        }
                        document.getElementById('priceSpan_'+stop_id).innerHTML = actual_price;                       
                        hide_spinner();
                        show_message(try_again_text);                        
                    }
                }
            })
            .catch(()=>{
               console.log('catch called - reload page')
               hide_spinner();
               show_message(reload_text);
            });
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
    }

    function  book_button_click(event){

        current_book_button = event.target;
        
         
        stop_id = event.target.dataset.stop_id;
        price = event.target.dataset.price ;
        vacant_months = event.target.dataset.vacant_months;

        // Opened order case
        if (order_id){
            current_book_button.removeEventListener('click', book_button_click)
            console.log('fetch put for opened order N =',order_id );
            months_to_book = '';

            // show spinner
            stops_page_message_container.classList.remove('invisible');
            spinner_container.classList.remove('invisible');
            close_icon3.classList.add('invisible');

            fetch_opened_order(stop_id, months_to_book , price, order_id);

        // brand  new  order case
        } else {
            console.log('order_id = ',order_id);                
            street = event.target.dataset.street;
            house = event.target.dataset.house;
                

            general_stops_container.classList.add('invisible');
            general_booking_container.classList.remove('invisible');
            submit_button.classList.remove('invisible');            
            booking_address_ul.classList.remove('invisible');
            spinner.classList.add('invisible');

            booking_address_ul.classList.remove('invisible');
            book_warning_message.classList.add('invisible');
            book_warning_message_1.classList.add('invisible');
            book_warning_message_2.classList.add('invisible');

            book_address.innerHTML = street + '&nbsp;' + house;
            book_price.innerHTML = price;
                        
            const vacant_months_arr= vacant_months.split(',');  
            
            count = 0;  l = vacant_months_arr.length;
            for (let month of vacant_months_arr){
                if(count < l/2 ){
                    create_checkbox(month,checkbox_container1 );
                } else {
                    create_checkbox(month,checkbox_container2 );
                }                
                count ++;
            }
            
            if (device === 'mobile'){
                set_parameters();
                window.addEventListener('resize', set_parameters);
            }

            // Clicking submit button
            submit_button.addEventListener('click', submit_checkbox);
            
            function submit_checkbox(){ 
                
                // warning mesage if anonymous_check
                if (app_explorer_username === 'anonymous_check'){
                    submit_button.classList.add('invisible');
                    book_warning_message.classList.remove('invisible');
                    booking_address_ul.classList.add('invisible');

                // getting input date    
                } else { 
                    book_warning_message_1.classList.add('invisible');                    
                    book_warning_message_2.classList.add('invisible');
                    months_to_book_arr = []
                    for (let month of vacant_months_arr){
                        if (document.getElementById(month).checked){
                            months_to_book_arr.push(month);
                        }
                    }
                    console.log(stop_id, months_to_book_arr);

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
                    if ( valid_choice ){   

                        submit_button.removeEventListener('click', submit_checkbox);

                        spinner.classList.remove('invisible');
                        booking_address_ul.classList.add('invisible');
                        submit_button.classList.add('invisible');

                        fetch_new_order(stop_id, months_to_book , price, order_id);

                        //  фетч -гет - отправить ИД бронируемой остановки, 
                        //              список номеров остановок отображаемых на данной странице
                        //          
                        //        получить подтверждение, что существует новый заказ
                        //          если да - обновить цифру в корзине, кнопку в Корзине
                        //                  получить актуальные book/info для всех отображаемых остановок
                        //                  актуализировать в html book/info на всей странице
                        //                  div  с выбором месяцев сбросить в первоначальное состояние
                        //                  спрятать спиннер, вернуться к списку остановок
                        //                  показать сообщение об успешном бронировании
                        //          если нет - получить актуальные цену , vacant_from, список вакантных
                        //                      месяцев
                        //                  div  с выбором месяцев сбросить в первоначальное состояние
                        //                  спрятать спиннер, вернуться к списку остановок
                        //                  оказать сообщение Try again



                    }                 
                }                
            }
        }    
    }













});