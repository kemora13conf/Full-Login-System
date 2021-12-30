const flash = document.getElementById("flash")
const close_flash = document.getElementById("close_flash")
const flash_container = document.getElementById('flash_container')


var animate_flash = ()=>{
    flash.setAttribute('class', 'flash animate_flash')
    setTimeout(()=>{
        flash_container.style.display = "none"
    }, 1000)
}

if (close_flash){
    close_flash.addEventListener('click', animate_flash)
}