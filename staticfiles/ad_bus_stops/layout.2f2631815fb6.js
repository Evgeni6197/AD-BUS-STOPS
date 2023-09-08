var portrait; 
var logo_container_height;

const layout_body = document.getElementById('layout_body')
const device = layout_body.dataset.device;
console.log(device);

const app_explorer_username = layout_body.dataset.app_explorer_username;
const template_name = layout_body.dataset.template_name;
const show_anonymous_message = layout_body.dataset.show_anonymous_message;
const show_registered_message = layout_body.dataset.show_registered_message

const logo = document.getElementById('logo');
const logo_container = document.getElementById('logo_container');
const nav_container = document.getElementById('nav_container');
const hello_container = document.getElementById('hello_container');
const study_registered_message_container = document.getElementById('study_registered_message_container')
const study_anonymous_message_container = document.getElementById('study_anonymous_message_container')
const top_container = document.getElementById('top_container');
const app_explorer_settings_templates = ['enter_app_explorer',
                                        'register_app_explorer',
                                        'app_explorer',
                                        'change_current_date'
                                        ].includes(template_name )
// set green background
if(app_explorer_settings_templates){
    top_container.classList.remove('bg_nav_blue');
    top_container.classList.add('bg_nav_green');
}

// show or hide warning message
if (show_registered_message == 'no'){
    hide_messages();
} else{

    if(! app_explorer_settings_templates && show_anonymous_message === 'True' ){

        if (app_explorer_username === 'anonymous_check'){
            study_registered_message_container.classList.add('invisible')
            study_anonymous_message_container.classList.remove('transparent')
        } else {
            study_registered_message_container.classList.remove('transparent')
            study_anonymous_message_container.classList.add('invisible')
        }
    } else {
        hide_messages();
    }
}

if (device === 'mobile'){   
    logo.classList.remove('logo_desktop');
    logo_size();
    window.addEventListener('resize', resize);
}
 
hello_container_size();

function resize(){
    logo_size();
    hello_container_size();
}

function logo_size() {

    portrait = window.innerWidth <  window.innerHeight;

    if (portrait){
        logo_container.classList.remove('col-3');
        logo_container.classList.add('col-6');
        nav_container.classList.remove('col-9');
        nav_container.classList.add('col-6'); 
        logo.classList.add('logo_mobile_portrait');
        logo.classList.remove('logo_mobile_landscape');    
    } else {
        logo_container.classList.add('col-3');
        logo_container.classList.remove('col-6');
        nav_container.classList.add('col-9');
        nav_container.classList.remove('col-6');
        logo.classList.remove('logo_mobile_portrait');
        logo.classList.add('logo_mobile_landscape');         
    }
}

function hello_container_size(){
    if (hello_container ){
        if (portrait){
            hello_container.style.height = '40px';
            hello_container.classList.remove('hello_container_landscape');
            hello_container.classList.add('hello_container_portrait');
        } else {
            logo_container_height = `${logo_container.offsetHeight}px`;
            hello_container.style.height = logo_container_height;
            hello_container.classList.add('hello_container_landscape');
            hello_container.classList.remove('hello_container_portrait');
        }   
    }
}
function hide_messages(){
    study_registered_message_container.classList.add('invisible');
    study_anonymous_message_container.classList.add('invisible');
}

