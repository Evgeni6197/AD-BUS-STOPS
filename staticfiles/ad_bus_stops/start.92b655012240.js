var interval_id;
var num = 0;
var containers = document.getElementsByClassName('start_container');

for(element of containers){  
    element.classList.add ('transparent');
}
console.log(77);

setLayout(); 

window.addEventListener('resize', setLayout);

function setLayout(){

    setDimensions();

    
    interval_id = setInterval(change_opacity,20);
    var currentOpacity;
    
}

function setDimensions(){

    const general_container = document.getElementById('general_container');
    let width_general = general_container.offsetWidth;
    //console.log('width_general=',width_general,general_container.offsetWidth);

    const three_photo_container = document.getElementById('three_photo_container');
    let width_3_photo = parseInt(window.getComputedStyle(three_photo_container).getPropertyValue("width"));

    //let width_3_photo = three_photo_container.offsetWidth;

    //const containers = document.getElementsByClassName('start_container');
    let width_1_photo = containers[0].offsetWidth;
    console.log('width_1_photo before cond ', containers[0].offsetWidth, 'width_3_photo= ', width_3_photo);
    const message_min_gap = 50;

    if (window.innerWidth < window.innerHeight) {

        //console.log('width_1_photo in portr', containers[0].offsetWidth);
        document.getElementById("pic_container3").classList.add('invisible');
        console.log('width_1_photo in portr ', containers[0].offsetWidth, 'width_3_photo= ', three_photo_container.offsetWidth);
        console.log(' ');

        if (width_1_photo *2.6 < window.innerHeight*0.95 - message_min_gap){
            // make visible second row of photos
            document.getElementById('two_photo_container').classList.remove('invisible');
        } else{
            document.getElementById('two_photo_container').classList.add('invisible');
        }

        // update width_1_photo after setting "pic_container3" invisible
        width_1_photo = containers[0].offsetWidth;

        for(element of containers){  
            element.style.height = width_1_photo * 1.3 + 'px' ;
        }

        //console.log("width_1_photo =", width_1_photo, window.innerWidth, width_general);
 
    } else {
        document.getElementById("pic_container3").classList.remove('invisible');
        document.getElementById('two_photo_container').classList.add('invisible');

        // for long and narrow viewport - shrink three_photo_container to force images fit 
        while (width_1_photo *1.3 > window.innerHeight*0.95-message_min_gap) {

            width_3_photo *= 0.99;
            three_photo_container.style.width = width_3_photo +'px';
            width_1_photo = containers[0].offsetWidth;

        }
/*
        while (width_1_photo *1.3+10 < window.innerHeight*0.95-message_min_gap && width_3_photo+10 < width_general){

            width_3_photo *= 1.01;
            three_photo_container.style.width = width_3_photo +'px';
            width_1_photo = containers[0].offsetWidth;
        }
*/


        for(element of containers){
            element.style.height = width_1_photo * 1.3 + 'px' ;
        }

        console.log('width_1_photo in lands ', containers[0].offsetWidth);
    }

    //console.log(containers[0].offsetWidth);

}
function change_opacity(){


    if (num < 100){
        currentOpacity = Number(window.getComputedStyle(containers[0]).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        containers[0].style.opacity = currentOpacity
        num ++;
    } else if( num >= 100 && num < 200){
        currentOpacity = Number(window.getComputedStyle(containers[1]).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        containers[1].style.opacity = currentOpacity
        num ++;
    } else if( num >= 200 && num < 300){
        currentOpacity = Number(window.getComputedStyle(containers[2]).getPropertyValue('opacity'));
        currentOpacity += 0.01;
        containers[2].style.opacity = currentOpacity
        num ++; 
    }
    else {
        clearInterval(interval_id);
    }

}