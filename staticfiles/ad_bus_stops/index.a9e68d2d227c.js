
document.addEventListener('DOMContentLoaded',()=>{

    const nav_wrap_container = document.getElementById('nav_wrap_container');
    const general_index_container = document.getElementById('general_index_container');
    
    var nav_wrap_containerHeight ;
    var portrait = window.innerWidth < window.innerHeight;
   
    set_orientaion_parameters();
    window.addEventListener('resize', resize);

    function set_orientaion_parameters(){

        if (portrait){
            general_index_container.classList.remove('bg_wide');
            general_index_container.classList.add('bg_narrow');
            set_height();    
        } else {
            general_index_container.classList.add('bg_wide');
            general_index_container.classList.remove('bg_narrow');
            set_height();
        }
    }
    function set_height(){
        nav_wrap_containerHeight = nav_wrap_container.offsetHeight;
        general_index_container.style.height = `${(window.innerHeight - nav_wrap_containerHeight)*0.99}px`    
    }
    function resize(){
        new_portrait = window.innerWidth < window.innerHeight;
        if (new_portrait != portrait){
            portrait = new_portrait;
            set_orientaion_parameters();            
        }
    }
})

