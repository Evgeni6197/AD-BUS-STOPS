console.log('portrait narrow'); 

// redirection on viewport orientation swap
var landscape;
window.addEventListener('resize', resize);

// get html elements
const two_photo_container_top = document.getElementsByClassName('two_photo_container')[0];
const two_photo_container_bottom = document.getElementsByClassName('two_photo_container')[1];
const pic_containers = document.getElementsByClassName('start_container');
const message_container = document.getElementById('message_container');

// store initial coordinates and dimentions in consts
const pic_container1X = pic_containers[0].offsetLeft;
const pic_container2X = pic_containers[1].offsetLeft;
const pic_containerY_top = pic_containers[0].offsetTop;
const pic_containerY_bottom  = pic_containers[3].offsetTop;
const pic_containerWidth = pic_containers[0].offsetWidth;
const pic_containerHeight = pic_containers[0].offsetHeight;
const message_containerX = message_container.offsetLeft;
const message_containerY = message_container.offsetTop;
const message_containerWidth = message_container.offsetWidth;
const message_containerHeight = message_container.offsetHeight;

// calculate value of  x-coordinate shift for one iteration
const deltaX = Math.floor((pic_container2X - pic_container1X)/30);

// set absolute coordinates for message container
message_container.classList.add('absolute');
message_container.style.left = `${message_containerX}px`;
message_container.style.top = `${message_containerY}px`;
message_container.style.width = `${message_containerWidth}px`;
message_container.style.height = `${message_containerHeight}px`;

// set absolute coordinates for initially visible image containers and change css accordingly
two_photo_container_top.classList.remove('row', 'align-items-center', 'justify-content-center');
two_photo_container_bottom.classList.remove('row', 'align-items-center', 'justify-content-center');
for (pic_container of pic_containers){
    pic_container.classList.remove('col');
    pic_container.classList.add('absolute');    
    pic_container.style.width = `${pic_containerWidth}px`;
    pic_container.style.height = `${pic_containerHeight}px`;
};
pic_containers[0].style.left = `${pic_container1X}px`;
pic_containers[1].style.left = `${pic_container2X}px`;
pic_containers[2].style.left = `${pic_container1X}px`;
pic_containers[3].style.left = `${pic_container2X}px`;
pic_containers[0].style.top = `${pic_containerY_top}px`;
pic_containers[1].style.top = `${pic_containerY_top}px`;
pic_containers[2].style.top = `${pic_containerY_bottom}px`;
pic_containers[3].style.top = `${pic_containerY_bottom}px`;

// animation
var interval_id;
var count = 0;
var currentOpacity;
var currentMessageOpacity ;
interval_id = setInterval(animation_frame,10);

function animation_frame(){
     
    if (count < 100){
        opacity_shift(0, 0.01);
    } else if( count >= 100 && count < 200){
        opacity_shift(1, 0.01);
    } else if( count >= 200 && count < 300){
        opacity_shift(2, 0.01);
    } else if( count >= 300 && count < 400){
        opacity_shift(3, 0.01);
    } else if( count >= 400 && count < 500){
        opacity_shift(0, -0.01);
    } else if( count >= 500 && count < 530){ 
        smooth_shift(1,500);   
    } else if( count === 530 ){ 
        finish_shift(1,4,'top');
    } else if( count >= 531 && count < 631){
        opacity_shift(4, 0.01);
    } else if( count >= 631 && count < 731){
        opacity_shift(2, -0.01);
    } else if( count >= 731 && count < 761){ 
        smooth_shift(3,731);    
    } else if( count === 761 ){ 
        finish_shift(3,5,'bottom'); 
    } else if( count >= 762 && count < 862){
        opacity_shift(5, 0.01);
    } else if( count >= 862 && count < 962){
        opacity_shift(1, -0.01);
    } else if( count >= 962 && count < 992){ 
        smooth_shift(4,962);    
    } else if( count === 992 ){ 
        finish_shift(4,6,'top');
    } else if( count >= 993 && count < 1093){
        opacity_shift(6, 0.01);
    } else if( count >= 1093 && count < 1193){
        opacity_shift(3, -0.01);
    } else if( count >= 1193 && count < 1223){ 
        smooth_shift(5,1193);    
    } else if( count === 1223 ){ 
        finish_shift(5,7,'bottom');         
    } else if( count >= 1224 && count < 1324){
        opacity_shift(7, 0.01);
    } else if( count >= 1324 && count < 1724 ){
        opacity_shift(4, -0.01);
        opacity_shift(5, -0.01);
        opacity_shift(6, -0.01);
        opacity_shift(7, -0.01);
        currentMessageOpacity = Number(window.getComputedStyle(message_container).getPropertyValue('opacity'));
        currentMessageOpacity += -0.01;
        message_container.style.opacity = currentMessageOpacity;
    } else if( count >= 1724 && count < 1754 ){
        count ++;
    } else {
        // stop animation and redirection to index page
        clearInterval(interval_id);   
        document.getElementById('to_index').click();      
    }
}

function opacity_shift(n,shift){   
    // changes opacity of n-th image container by 'shift' value
    currentOpacity = Number(window.getComputedStyle(pic_containers[n]).getPropertyValue('opacity'));
    currentOpacity += shift;
    pic_containers[n].style.opacity = currentOpacity;
    count ++;
}
function smooth_shift(n,start){
    pic_containers[n].style.left = `${pic_container2X - deltaX * (count - start)}px`;
    count ++; 
}
function finish_shift(n,m,place){
    // setting initial absolute x-coordinates to finish smooth shifting accurately
    pic_containers[n].style.left = `${pic_container1X}px`;
    pic_containers[m].style.left = `${pic_container2X}px`;
    pic_containers[m].classList.remove('invisible');
    count ++; 
    if (place === 'top'){
        pic_containers[m].style.top = `${pic_containerY_top}px`;
    } else {
        pic_containers[m].style.top = `${pic_containerY_bottom}px`;
    }
}

function resize(){
    //redirection works only if viewport orientaion changes
    landscape = window.innerWidth >  window.innerHeight;
    if (landscape){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
} 