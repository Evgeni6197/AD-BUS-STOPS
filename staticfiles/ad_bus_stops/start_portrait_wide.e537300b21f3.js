console.log('portrait_wide');

// redirection on viewport orientation swap
var landscape;
window.addEventListener('resize', resize);

// get html elements
const two_photo_container = document.getElementsByClassName('two_photo_container')[0];
const pic_containers = document.getElementsByClassName('start_container');
const message_container = document.getElementById('message_container');

// store initial coordinates and dimentions in consts
const pic_container1X= pic_containers[0].offsetLeft;
const pic_container2X= pic_containers[1].offsetLeft;
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
two_photo_container.classList.remove('row', 'align-items-center', 'justify-content-center');
for (pic_container of pic_containers){
    pic_container.classList.remove('col');
    pic_container.classList.add('absolute');
    pic_container.style.top = `${pic_containerY}px`;
    pic_container.style.width = `${pic_containerWidth}px`;
    pic_container.style.height = `${pic_containerHeight}px`;
};
pic_containers[0].style.left = `${pic_container1X}px`;
pic_containers[1].style.left = `${pic_container2X}px`;

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
        opacity_shift(0, -0.01);
    } else if( count === 300 ){
        pic_containers[0].classList.add('invisible');
        count ++;
    } else if( count >= 301 && count < 331){ 

        // smooth x-coordinate shift 
        pic_containers[1].style.left = `${pic_container2X - deltaX * (count - 301)}px`;
        count ++;     
    } else if( count === 331 ){ 

        // setting initial absolute x-coordinates to finish smooth shifting accurately
        pic_containers[1].style.left = `${pic_container1X}px`;
        pic_containers[2].style.left = `${pic_container2X}px`;
        pic_containers[2].classList.remove('invisible');
        count ++; 
    } else if( count > 331 && count <= 431 ){
        opacity_shift(2, 0.01);
    } else if( count > 431 && count <= 531 ){
        opacity_shift(1, -0.01); 
    } else if( count === 532 ){
        pic_containers[1].classList.add('invisible');
        count ++; 
    } else if( count >= 533 && count < 563){ 

        // smooth x-coordinate shift 
        pic_containers[2].style.left = `${pic_container2X - deltaX * (count - 533)}px`;
        count ++;  
    } else if( count === 563 ){ 

        // setting initial absolute x-coordinates to finish smooth shifting accurately
        pic_containers[2].style.left = `${pic_container1X}px`;
        pic_containers[3].style.left = `${pic_container2X}px`;
        pic_containers[3].classList.remove('invisible');
        count ++; 
    } else if( count > 563 && count <= 663 ){
        opacity_shift(3, 0.01);
    } else if( count > 663 && count <= 763 ){
        opacity_shift(2, -0.01); 
    } else if( count === 764 ){
        pic_containers[2].classList.add('invisible');
        count ++; 
    } else if( count >= 765 && count < 795){ 

        // smooth x-coordinate shift 
        pic_containers[3].style.left = `${pic_container2X - deltaX * (count - 765)}px`;
        count ++;  
    } else if( count === 795 ){ 

        // setting initial absolute x-coordinates to finish smooth shifting accurately
        pic_containers[3].style.left = `${pic_container1X}px`;
        pic_containers[4].style.left = `${pic_container2X}px`;
        pic_containers[4].classList.remove('invisible');
        count ++; 
    } else if( count > 795 && count <= 895 ){
        opacity_shift(4, 0.01);
    } else if( count > 895 && count <= 1095 ){
        opacity_shift(4, -0.01);
        opacity_shift(3, -0.01);
        currentMessageOpacity = Number(window.getComputedStyle(message_container).getPropertyValue('opacity'));
        currentMessageOpacity += -0.01;
        message_container.style.opacity = currentMessageOpacity;
    } else if( count > 1095 && count <= 1145 ){
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

function resize(){

    //redirection works only if viewport orientaion changes
    landscape = window.innerWidth >  window.innerHeight;
    if (landscape){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
}  