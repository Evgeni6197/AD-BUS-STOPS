function main_action(){

    console.log('stops') ;
    const layout_body = document.getElementById('layout_body');
    const device = layout_body.dataset.device;
    const price_containers = document.querySelectorAll('.price_container');

    if (device === 'desktop'){
        price_containers.forEach((element)=>{element.classList.add('set_border'); });
    } else {
        const top_stops_container = document.getElementById('top_stops_container');
        const search_container = document.getElementById('search_container');
        const cart_container = document.getElementById('cart_container'); 
        
        const date_containers = document.querySelectorAll('.date_container');        
        const book_btn_containers = document.querySelectorAll('.book_btn_container');
        var portrait ;

        set_parameters();
        window.addEventListener('resize', set_parameters);

        function set_parameters(){

            layout_body.classList.add('transparent');
            portrait = window.innerWidth <  window.innerHeight;

            if (portrait){
                top_stops_container.innerHTML = '';
                top_stops_container.appendChild(cart_container);
                top_stops_container.appendChild(search_container);

                top_stops_container.classList.remove('row');
                search_container.classList.remove('col-7');
                cart_container.classList.remove('col-5');

                date_containers.forEach((element)=>{element.classList.add('invisible'); });               
                price_containers.forEach((element)=>{element.classList.remove('col-1'); });
                price_containers.forEach((element)=>{element.classList.add('col-3');    });                  
                book_btn_containers.forEach((element)=>{element.classList.remove('col-2'); });
                book_btn_containers.forEach((element)=>{element.classList.add('col-3');    }); 
            } else {
                top_stops_container.innerHTML = '';
                top_stops_container.appendChild(search_container);
                top_stops_container.appendChild(cart_container);
                
                top_stops_container.classList.add('row');
                search_container.classList.add('col-7');
                cart_container.classList.add('col-5');

                date_containers.forEach((element)=>{element.classList.remove('invisible'); });               
                price_containers.forEach((element)=>{element.classList.add('col-1'); });
                price_containers.forEach((element)=>{element.classList.remove('col-3');    });                  
                book_btn_containers.forEach((element)=>{element.classList.add('col-2'); });
                book_btn_containers.forEach((element)=>{element.classList.remove('col-3');    }); 
            }
            layout_body.classList.remove('transparent');
        }
    }
}

document.addEventListener('DOMContentLoaded', main_action);