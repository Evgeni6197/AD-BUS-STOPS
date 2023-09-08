setLayout();
  
window.addEventListener('resize', adjustLayout);

function appear(n){

    const pic_container = document.getElementById(`pic_container${n}`)

    pic_container.classList.remove('initial');
    pic_container.classList.add('animated');
}

function portrait(){
    document.getElementById("pic_container3").classList.add('invisible');
    document.getElementById("pic_container5").classList.remove('invisible');
    document.getElementById("pic_container4").classList.remove('invisible');
    document.getElementById('message_container').classList.add('transparent');
}

function landscape(){
    document.getElementById("pic_container3").classList.remove('invisible');
    document.getElementById("pic_container5").classList.add('invisible');
    document.getElementById("pic_container4").classList.add('invisible');
    document.getElementById('message_container').classList.add('transparent');
}

function setLayout() {

    if (window.innerWidth < window.innerHeight) {
        
        document.getElementById("pic_container3").classList.add('invisible');
   
        appear(2);
        setTimeout(()=>{appear(1)},2000);
        setTimeout(()=>{appear(4)},4000);
        setTimeout(()=>{appear(5)},6000);
        setTimeout(appear_message,8000);

    } else {
        document.getElementById("pic_container5").classList.add('invisible');
        document.getElementById("pic_container4").classList.add('invisible');
        appear(2);
        setTimeout(()=>{appear(1)},2000);
        setTimeout(()=>{appear(3)},4000);
        setTimeout(appear_message,6000);
    }
  }

function adjustLayout() {

    document.getElementById("pic_container1").classList.add('initial');
    document.getElementById("pic_container2").classList.add('initial');

    if (window.innerWidth < window.innerHeight) {
        
        portrait();
   
        appear(2);
        setTimeout(()=>{appear(1)},2000);
        setTimeout(()=>{appear(4)},4000);
        setTimeout(()=>{appear(5)},6000);


    } else {
        
        landscape();
        appear(2);
        setTimeout(()=>{appear(1)},2000);
        setTimeout(()=>{appear(3)},4000);
    }
  }

  function appear_message(){
    const message_container = document.getElementById('message_container');
    message_container.classList.remove('transparent');
    message_container.classList.add('animated');
  }

  