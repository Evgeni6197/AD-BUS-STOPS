// check type of layout:  landscape or portrait  and  mobile or not 
const initial_device_orientation = document.getElementById('viewport1').dataset.device;
console.log(initial_device_orientation); 
var current_device_orientation; 

// redirection on viewport orientation swap
var portrait;
window.addEventListener('resize', resize);

// get html elements
const general_container = document.getElementById('general_container_mobile');
const wrapping_container = document.getElementById('wrapping_container');
const pic_containers = document.getElementsByClassName('start_container');
const message_container = document.getElementById('message_container');
const button_container = document.getElementById('button_container');
const text_container = document.getElementById('text_container');
const button = document.getElementById('button');

// store initial coordinates and dimensions  of  general_container in consts
const general_containerX = general_container.offsetLeft;
const general_containerY = general_container.offsetTop;
const general_containerWidth = general_container.offsetWidth;
const general_containerHeight = general_container.offsetHeight;

// store initial coordinates and dimensions  of  wrapping_container in consts
const wrapping_containerX = wrapping_container.offsetLeft;
const wrapping_containerY = wrapping_container.offsetTop;
const wrapping_containerWidth = wrapping_container.offsetWidth;
const wrapping_containerHeight = wrapping_container.offsetHeight;

// store initial coordinates and dimensions  of  image and message containers in consts
const pic_container1X= pic_containers[0].offsetLeft - 37; // '37' ajusting parameter
const pic_containerY= pic_containers[0].offsetTop;
const pic_containerWidth = pic_containers[0].offsetWidth;
const pic_containerHeight = pic_containers[0].offsetHeight;
const message_containerX = message_container.offsetLeft;
const message_containerY = message_container.offsetTop;
const message_containerWidth = message_container.offsetWidth;
const message_containerHeight = message_container.offsetHeight;

// calculate initial x-coordinate of 2nd container
const pic_container2X= pic_container1X + pic_containerWidth +17; // '17' ajusting parameter

// calculate value of  x-coordinate shift for one iteration
const deltaX = Math.floor((pic_container2X - pic_container1X)/92);

// set absolute coordinates for wrapping container and change css accordingly
wrapping_container.classList.remove( 'wrapping_initial');
wrapping_container.classList.add('absolute');
wrapping_container.style.left = `${wrapping_containerX}px`;
wrapping_container.style.top = `${wrapping_containerY}px`;
wrapping_container.style.width =`${wrapping_containerWidth}px`;
wrapping_container.style.height = `${wrapping_containerHeight}px`;

// set absolute coordinates for initially visible image container and change css accordingly
for (pic_container of pic_containers){
    pic_container.classList.add('absolute');
    pic_container.style.top = `${pic_containerY-18}px`;  // '18' ajusting parameter
    pic_container.style.width = `${pic_containerWidth}px`;
    pic_container.style.height = `${pic_containerHeight}px`;
}

// set new absolute coordinates for message container  - for initial animation phase
message_container.classList.add('absolute');
button_container.classList.add('invisible');
message_container.classList.remove('message_container');
message_container.style.left = `${general_containerX}px`;
message_container.style.top = `${general_containerY}px`;
message_container.style.width =`${ general_containerWidth}px`;
message_container.style.height =`${ general_containerHeight}px`;

// set new absolute coordinates for text_container
text_container.style.left = `${general_containerX}px`;
text_container.style.top = `${general_containerY}px`;
text_container.style.width =`${ general_containerWidth}px`;
text_container.style.height =`${ general_containerHeight}px`;

// skip front page
general_container.addEventListener('click',to_app_explorer);

// animation
var interval_id;
var count = -700;
var currentOpacity;
var currentMessageOpacity ;
var currentTextOpacity;
interval_id = setInterval(animation_frame,15);


function animation_frame(){ 

    if (count >= -700 && count <= -500){
        message_change_opacity(0.005);        
    } else if (count > -500 && count <= -400){
        count ++; 
    } else if (count > -400 && count <= -300){
        message_change_opacity(-0.01);
    } else if (count > -300 && count < -200){
        text_change_opacity(0.02);        
    } else if( count === -200){ 
        // return to old  absolute coordinates for message container          
        message_container.classList.add('message_container');
        button_container.classList.remove('invisible');
        message_container.style.left = `${message_containerX}px`;
        message_container.style.top = `${message_containerY}px`;
        message_container.style.width = `${message_containerWidth}px`;
        message_container.style.height = `${message_containerHeight}px`;
        // 
        initialize(0);
    } else if (count > -200 && count <= -100){
      count++
    } else if (count > -100 && count <= 0){
        text_change_opacity(-0.01);           
    } else if (count > 0 && count <= 100){
        opacity_shift(0, 0.01);
        message_change_opacity(0.01);
        count --;
    } else if (count >100 && count <= 150){
        count++
    } else if( count > 150 && count < 250){
        smooth_shift(0,150);
    } else if( count ===  250){
        initialize(1);
    } else if( count > 250 && count < 350){ 
        smooth_shift(1,250); 
    } else if( count ===  350){
        initialize(2);
    } else if( count >350 && count < 450){ 
        smooth_shift(2,350);         
    } else if( count ===  450){
        initialize(3); 
    } else if( count > 450 && count < 550){ 
        smooth_shift(3,450); 
    } else if( count >= 550 && count < 850){
        opacity_shift(3, -0.01);
        opacity_shift(4, -0.01);
        message_change_opacity(-0.01);                    
    } else {
        // stop animation and redirection to index page
        clearInterval(interval_id); 
        to_app_explorer();       
    }
}
function message_change_opacity(shift){
    currentMessageOpacity = Number(window.getComputedStyle(message_container).getPropertyValue('opacity'));
    currentMessageOpacity += shift;
    message_container.style.opacity = currentMessageOpacity;
    count ++;
}
function text_change_opacity(shift){
    currentTextOpacity = Number(window.getComputedStyle(text_container).getPropertyValue('opacity'));
    currentTextOpacity += shift;
    text_container.style.opacity = currentTextOpacity;
    count ++;
}

function opacity_shift(n,shift){    
    // changes opacity of n-th image container by 'shift' value
    currentOpacity = Number(window.getComputedStyle(pic_containers[n]).getPropertyValue('opacity'));
    currentOpacity += shift;
    pic_containers[n].style.opacity = currentOpacity;
    count ++;
}

function smooth_shift(n,start){
    // smooth x-coordinate shift 
    pic_containers[n].style.left = `${pic_container1X - deltaX * (count - start)}px`;
    pic_containers[n+1].style.left = `${pic_container2X - deltaX * (count - start)}px`;
    count ++;
}
function initialize(n){
    //pic_containers[n].style.left = `${pic_container1X}px`;
    pic_containers[n+1].classList.remove('invisible');
    pic_containers[n+1].style.left = `${pic_container2X}px`; 
    count ++;  
}

function resize(){
    //redirection works only if viewport orientaion changes
    portrait = window.innerWidth <  window.innerHeight;
    if(portrait){
        current_device_orientation = 'mobile_portrait';
    } else {
        current_device_orientation = 'mobile_landscape';
    }
    if (current_device_orientation !== initial_device_orientation){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
} 
function to_app_explorer(){
    document.getElementById('to_app_explorer').click();
}