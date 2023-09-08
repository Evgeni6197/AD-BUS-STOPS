
const register_form = document.getElementById('register_form');
const register_button = document.getElementById('register_button');
const animation_container = document.getElementById('animation_container');
const register_form_container=document.getElementById('register_form_container');


register_form.addEventListener('submit',()=>{

    register_button.disabled = true;
    animation_container.classList.remove('invisible');
    register_form_container.classList.add('invisible');
})