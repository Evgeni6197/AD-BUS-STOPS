
document.addEventListener('DOMContentLoaded',()=>{

    const nav_wrap_container = document.getElementById('nav_wrap_container');
    const general_index_container = document.getElementById('general_index_container');
    const index_text_container = document.getElementById('index_text_container');
    const wrapping_index = document.getElementById('wrapping_index');
    const count = index_text_container.dataset.count;
    const device = index_text_container.dataset.device;

    const first_col = document.getElementById('first_col');
    const second_col = document.getElementById('second_col');
    const third_col = document.getElementById('third_col');
    const fourth_col = document.getElementById('fourth_col');
    const mob_narr_link = document.getElementById('mob_narr_link');

    var nav_wrap_containerHeight ;
    var h;
    var portrait = window.innerWidth < window.innerHeight;
   
    set_orientaion_parameters();
    wrapping_index.classList.remove('transparent');
    window.addEventListener('resize', resize);

    // animation
    var interval_id;
    var letter_id = 0;
    interval_id = setInterval(animation_frame,50);

    function animation_frame(){
        if (letter_id < count){
            document.getElementById(letter_id).classList.remove('transparent');
            letter_id ++;
        } else {
            clearInterval(interval_id); 
        }
    }
    function set_orientaion_parameters(){

        if (portrait){
            general_index_container.classList.remove('bg_wide');
            general_index_container.classList.add('bg_narrow');
            set_height(); 
            if (device === 'mobile'){
                first_col.classList.add('invisible');
                second_col.classList.add('invisible');
                third_col.classList.add('invisible');
                fourth_col.classList.remove('col-5');
                mob_narr_link.classList.remove('invisible');
            }
        } else {
            general_index_container.classList.add('bg_wide');
            general_index_container.classList.remove('bg_narrow');
            set_height();
            if (device === 'mobile'){
                first_col.classList.remove('invisible');
                second_col.classList.remove('invisible');
                third_col.classList.remove('invisible');
                fourth_col.classList.add('col-5');
                mob_narr_link.classList.add('invisible');
            }           
        }
    }
    function set_height(){
        nav_wrap_containerHeight = nav_wrap_container.offsetHeight;
        h = (window.innerHeight - nav_wrap_containerHeight)
        general_index_container.style.height = `${h*0.99}px`  
        index_text_container.style.height = `${h*0.95}px`  
    }
    function resize(){
        new_portrait = window.innerWidth < window.innerHeight;
        if (new_portrait != portrait){
            portrait = new_portrait;
            set_orientaion_parameters();            
        }
    }
})

