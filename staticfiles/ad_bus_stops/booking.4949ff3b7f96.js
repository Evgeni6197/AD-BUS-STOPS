document.addEventListener('DOMContentLoaded', ()=>{

    console.log('booking')
    const layout_body = document.getElementById('layout_body');
    const nav_wrap_container = document.getElementById('nav_wrap_container');
    const app_explorer_username = layout_body.dataset.app_explorer_username;
    const device = layout_body.dataset.device;

    const book_buttons = document.querySelectorAll('.book_button');
    const cart_button = document.getElementById('cart_button');
    const general_booking_container = document.getElementById('general_booking_container');
    const general_stops_container = document.getElementById('general_stops_container');
    const general_cart_container = document.getElementById('general_cart_container');
    const book_address = document.getElementById('book_address');
    const book_price = document.getElementById('book_price');

    const checkbox_container1 = document.getElementById('checkbox_container1');
    const checkbox_container2 = document.getElementById('checkbox_container2');
    const submit_button = document.getElementById('submit_button');
    const return_button = document.getElementById('return_button');
    const booking_address_ul = document.getElementById('booking_address_ul');    
    const close_icon1 = document.getElementById('close_icon1');
    const close_icon2 = document.getElementById('close_icon2');

    const order_id = cart_button.dataset.order_id
    const checkbox_wrapping_container = document.getElementById('checkbox_wrapping_container');
    const spinner = document.getElementById('spinner');
    const book_warning_message = document.getElementById('book_warning_message');
    const book_warning_message_1 = document.getElementById('book_warning_message_1');
    const book_warning_message_2 = document.getElementById('book_warning_message_2');

    var vacant_months, stop_id, street, house, price,  month_arr, months_to_book_arr, months_to_book;
    var temp, count, valid_choice, portrait, target_container, l, h;

    close_icon1.addEventListener('click',()=>{
        book_warning_message_1.classList.add('invisible');
    })
    close_icon2.addEventListener('click',()=>{
        book_warning_message_2.classList.add('invisible');
    })

    book_buttons.forEach((element)=>{

        // Clicking  book button
        element.addEventListener('click',(event)=>{

            vacant_months = event.target.dataset.vacant_months;
            stop_id = event.target.dataset.stop_id;
            street = event.target.dataset.street;
            house = event.target.dataset.house;
            price = event.target.dataset.price ;  

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
                
                //submit_button.removeEventListener('click', submit_checkbox);
                
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

                        fetch('/book',{
                            'method'  : 'PUT',
                            'body': JSON.stringify({
                                        stop_id: stop_id,
                                        months_to_book: months_to_book,
                                        price: price,
                            })
                        });
                    }                   
                }                
            }
        });
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
        //newCheckboxInput.style.backgroundColor = 'green';
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
        console.log(h,window.innerHeight);
        checkbox_wrapping_container.style.height = `${(window.innerHeight-h)*0.85}px`
    }

});