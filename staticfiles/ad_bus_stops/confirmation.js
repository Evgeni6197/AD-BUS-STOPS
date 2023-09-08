document.addEventListener('DOMContentLoaded',()=>{

    const time_left = document.getElementById('heading').dataset.time_left;
    const timer_container = document.getElementById('timer_container');
    const link = document.getElementById('link');

    var timer = parseInt(time_left);
    var interval_id;
    interval_id = setInterval(timer_func,1000);


    function timer_func(){
        
        if (timer > 0){
            timer_container.innerHTML = 'Left  '+timer+' sec';
            timer --;
        } else {
            link.click();
        }
    }
});