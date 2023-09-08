var portrait; 
var logo_container_height;

const device = document.getElementById('layout_body').dataset.device;
console.log(device);

const logo = document.getElementById('logo');
const logo_container = document.getElementById('logo_container');
const nav_container = document.getElementById('nav_container');
const hello_container = document.getElementById('hello_container');

if (device === 'mobile'){   
    logo.classList.remove('logo_desktop');
    logo_size();
    window.addEventListener('resize', resize);
};
 
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
        };    
    };
}