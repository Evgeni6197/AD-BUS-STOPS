console.log('landscape');

// redirection on viewport orientation swap
var portrait;
window.addEventListener('resize', resize);

// get html elements
const three_photo_container = document.getElementById('three_photo_container');
const pic_containers = document.getElementsByClassName('start_container');
const message_container = document.getElementById('message_container');


// store initial coordinates and dimentions in consts
const pic_container1X= pic_containers[0].offsetLeft;
const pic_container2X= pic_containers[1].offsetLeft;
const pic_container3X= pic_containers[2].offsetLeft;
const pic_containerY= pic_containers[0].offsetTop;
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
three_photo_container.classList.remove('row', 'align-items-center', 'justify-content-center');
for (pic_container of pic_containers){
    pic_container.classList.remove('col');
    pic_container.classList.add('absolute');
    pic_container.style.top = `${pic_containerY}px`;
    pic_container.style.width = `${pic_containerWidth}px`;
    pic_container.style.height = `${pic_containerHeight}px`;
};
pic_containers[0].style.left = `${pic_container1X}px`;
pic_containers[1].style.left = `${pic_container2X}px`;
pic_containers[2].style.left = `${pic_container3X}px`;

// animation
var interval_id;
var count = 0;
var currentOpacity;
var currentMessageOpacity ;
interval_id = setInterval(animation_frame,15);

function animation_frame(){
     
    if (count < 100){
        opacity_shift(0, 0.01);
    } else if( count >= 100 && count < 200){
        opacity_shift(1, 0.01);
    } else if( count >= 200 && count < 300){
        opacity_shift(2, 0.01);
    } else if (count >=300 && count<400){
        opacity_shift(0, -0.01);
    } else if( count === 400 ){
        set_invisible(0);
    } else if( count >= 400 && count < 432){ 
        smooth_shift(1,400);
    } else if( count === 432 ){ 
        finish_shift(1); 
    } else if( count > 432 && count <= 532 ){
        opacity_shift(3, 0.01);
    } else if( count > 532 && count <= 632 ){
        opacity_shift(1, -0.01); 
    } else if( count === 633 ){
        set_invisible(1);
    } else if( count >= 634 && count < 664){ 
        smooth_shift(2,634);
    } else if( count === 664 ){ 
        finish_shift(2); 
    } else if( count > 664 && count <= 764 ){
        opacity_shift(4, 0.01);
    } else if( count > 764 && count <= 1064 ){   
        opacity_shift(4, -0.01);
        opacity_shift(3, -0.01);
        opacity_shift(2, -0.01);
        currentMessageOpacity = Number(window.getComputedStyle(message_container).getPropertyValue('opacity'));
        currentMessageOpacity += -0.01;
        message_container.style.opacity = currentMessageOpacity;
    } else if( count > 1064 && count <= 1094 ){
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
function set_invisible(n){
    pic_containers[n].classList.add('invisible');
    count ++;
}
function smooth_shift(n,start){
    // smooth x-coordinate shift 
    pic_containers[n].style.left = `${pic_container2X - deltaX * (count - start)}px`;
    pic_containers[n+1].style.left = `${pic_container3X - deltaX * (count - start)}px`;
    count ++; 
}
function finish_shift(n){
    // setting initial absolute x- coordinates to finish smooth shifting accurately
    pic_containers[n].style.left = `${pic_container1X}px`;
    pic_containers[n+1].style.left = `${pic_container2X}px`;
    pic_containers[n+2].style.left = `${pic_container3X}px`;
    pic_containers[n+2].classList.remove('invisible');
    count ++;  
}
function resize(){
    //redirection works only if viewport orientaion changes
    portrait = window.innerWidth <  window.innerHeight;
    if (portrait){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
}
