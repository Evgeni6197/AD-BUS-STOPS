
console.log('landscape');

console.log(8992);

var portrait;

window.addEventListener('resize', ()=>{

    //redirection works only if viewport orientaion changes
    portrait = window.innerWidth <  window.innerHeight;
    if (portrait){
        resize_link = document.getElementById('resize');
        resize_link.href = '/';
        resize_link.click();
    }
}); 

var interval_id;
var count;
var currentOpacity;

const three_photo_container = document.getElementById('three_photo_container');
const pic_containers = document.getElementsByClassName('start_container');
const message_container = document.getElementById('message_container');

const pic_container1X= pic_containers[0].offsetLeft;
const pic_container2X= pic_containers[1].offsetLeft;
const pic_container3X= pic_containers[2].offsetLeft;

const pic_containerY= pic_containers[0].offsetTop;
const pic_containerWidth = pic_containers[0].offsetWidth;
const pic_containerHeight = pic_containers[0].offsetHeight;

const deltaX = Math.floor((pic_container2X - pic_container1X)/30);

const message_containerX = message_container.offsetLeft;
const message_containerY = message_container.offsetTop;
const message_containerWidth = message_container.offsetWidth;
const message_containerHeight = message_container.offsetHeight;


message_container.classList.add('absolute');
message_container.style.left = `${message_containerX}px`;
message_container.style.top = `${message_containerY}px`;
message_container.style.width = `${message_containerWidth}px`;
message_container.style.height = `${message_containerHeight}px`;

animate_once();

function animate_once(){

count = 0;  

interval_id = setInterval(change_opacity,20);
}

function change_opacity(){
    
    
    if (count < 100){
        opacity_shift(0, 0.01);
    } else if( count >= 100 && count < 200){
        opacity_shift(1, 0.01);
    } else if( count >= 200 && count < 300){
        opacity_shift(2, 0.01);
    } else if (count >=300 && count<400){
        opacity_shift(0, -0.01);
    } else if( count === 400 ){
        pic_containers[0].classList.add('invisible');
        
        three_photo_container.classList.remove('row',  'align-items-center', 'justify-content-center' );
        for (pic_container of pic_containers){
            pic_container.classList.remove('col');
            pic_container.classList.add('absolute');

            pic_container.style.top = `${pic_containerY}px`;
            pic_container.style.width = `${pic_containerWidth}px`;
            pic_container.style.height = `${pic_containerHeight}px`;
        }

        pic_containers[1].style.left = `${pic_container2X}px`;
        pic_containers[2].style.left = `${pic_container3X}px`;

        count ++;

    } else if( count >= 400 && count < 432){ 
        pic_containers[1].style.left = `${pic_container2X - deltaX * (count - 400)}px`;
        pic_containers[2].style.left = `${pic_container3X - deltaX * (count - 400)}px`;
        count ++;     

    } else if( count === 432 ){ 

        pic_containers[3].style.left = `${pic_container3X}px`;
        pic_containers[3].classList.remove('invisible');

        count ++;  

    } else if( count > 432 && count < 532 ){
   
        opacity_shift(3, 0.01);
  
        
        
    } else {
        clearInterval(interval_id);
    }

}

function opacity_shift(n,shift){
    currentOpacity = Number(window.getComputedStyle(pic_containers[n]).getPropertyValue('opacity'));
    currentOpacity += shift;
    pic_containers[n].style.opacity = currentOpacity;
    count ++;
}
