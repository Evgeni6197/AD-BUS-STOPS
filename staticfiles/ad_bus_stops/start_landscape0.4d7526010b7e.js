//variant of working animation and jump to new position

console.log('landscape');

console.log(478);

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

const pic_container1 = document.getElementById('pic_container1');
const pic_container2 = document.getElementById('pic_container2');
const pic_container3 = document.getElementById('pic_container3');
const pic_container4 = document.getElementById('pic_container4');

const pic_container1X= pic_container1.offsetLeft;
const pic_container1Y= pic_container1.offsetTop;
const pic_container2X= pic_container2.offsetLeft;
const pic_container2Y= pic_container2.offsetTop;
const pic_container3X= pic_container3.offsetLeft;
const pic_container3Y= pic_container3.offsetTop;

const deltaX = Math.floor((pic_container2X - pic_container1X)/30);
 


animate_once();

function animate_once(){

count = 0;  

interval_id = setInterval(change_opacity,20);
}

function change_opacity(){
    
    
    if (count < 100){
        currentOpacity = Number(window.getComputedStyle(pic_container1).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        pic_container1.style.opacity = currentOpacity;
        count ++;
    } else if( count >= 100 && count < 200){
        currentOpacity = Number(window.getComputedStyle(pic_container2).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        pic_container2.style.opacity = currentOpacity;
        count ++;
    } else if( count >= 200 && count < 300){
        currentOpacity = Number(window.getComputedStyle(pic_container3).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        pic_container3.style.opacity = currentOpacity;
        count ++; 
    
    } else if (count >=300 && count<400){
        currentOpacity = Number(window.getComputedStyle(pic_container1).getPropertyValue('opacity'));
        currentOpacity -= 0.01;
        pic_container1.style.opacity = currentOpacity;
        count ++;

    } else if( count === 400 ){
        pic_container1.classList.add('invisible');
        pic_container4.classList.remove('invisible');
        count ++;
        
    } else if( count > 400 && count < 500){
        currentOpacity = Number(window.getComputedStyle(pic_container4).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        pic_container4.style.opacity = currentOpacity;
        count ++;
    } else if( count >= 500 && count < 530){ 
        count ++; 
        
        
    } else {
        clearInterval(interval_id);
        console.log('end one cycle')
    }

}


