setLayout();

window.addEventListener('resize', setLayout);

function setLayout() {
    const containers = document.getElementsByClassName('start_container');
    for (element of containers){
        element.classList.add('transparent');
    }

    //const containers = document.querySelectorAll('.start_container');
    //containers.forEach((element)=>{
        //element.classList.add('transparent');
    //});
    document.getElementById('message_container').classList.add('transparent');

    if (window.innerWidth < window.innerHeight) {

        document.getElementById("pic_container3").classList.add('invisible');
        document.getElementById("pic_container5").classList.remove('invisible');
        document.getElementById("pic_container4").classList.remove('invisible');


        for(element of containers){
            const width = (window.innerWidth * 0.95 - 20)/2;
            element.style.width = width + 'px'
            element.style.height = width * 1.3 + 'px' ;
        }
        //containers.forEach((element)=>{
        //    const width = (window.innerWidth * 0.95 - 20)/2;
        //    element.style.width = width + 'px'
        //    element.style.height = width * 1.3 + 'px' ;
        //});       
 

        appear(1);
        setTimeout(()=>{appear(2)},1000);
        setTimeout(()=>{appear(4)},2000);
        setTimeout(()=>{appear(5)},3000);
        setTimeout(appear_message,4000);

    } else {

        document.getElementById("pic_container3").classList.remove('invisible');
        document.getElementById("pic_container5").classList.add('invisible');
        document.getElementById("pic_container4").classList.add('invisible');

        for(element of containers){
            const width = (window.innerWidth * 0.95 - 30)/3;
            element.style.width = width + 'px'
            element.style.height = width * 1.3 + 'px' ;
        }



        //containers.forEach((element)=>{
        //    const width = (window.innerWidth * 0.95 - 30)/3;
        //    element.style.width = width + 'px'
        //    element.style.height = width * 1.3 + 'px' ;
        //});

        appear(1);
        setTimeout(()=>{appear(2)},1000);
        setTimeout(()=>{appear(3)},2000);
        setTimeout(appear_message,3000);
    }
  }

  function appear(n){
    const pic_container = document.getElementById(`pic_container${n}`)
    pic_container.classList.remove('transparent');
    pic_container.classList.add('animated');
}

  function appear_message(){
    const message_container = document.getElementById('message_container');
    message_container.classList.remove('transparent');
    message_container.classList.add('animated');
  }

  