window_width = window.innerWidth

// Control buttons
const next1 = document.querySelector('#next1')
const next2 = document.querySelector('#next2')
const back1 = document.querySelector('#back1')
const back2 = document.querySelector('#back2')

// Picture import elements
const file = document.querySelector('#file')
const imp_btn = document.querySelector('#import_pic_btn')
const pic_name = document.querySelector('#pic_name')
const img = document.querySelector('#img')

imp_btn.addEventListener('click', ()=>{
    file.click()
})
var import_image = ()=>{
    var reader = new FileReader()
    reader.onload = ()=>{
        img.setAttribute('src', reader.result)
    }
    reader.readAsDataURL(file.files[0])
    pic_name.innerHTML = file.value.slice(12)
}
file.addEventListener('change', import_image, false)


// Function to slide the forms
var slide_next = (e)=>{
    e.parentElement.parentElement.style.marginLeft = "-350px"
}
var slide_back = (e)=>{
    e.parentElement.parentElement.previousElementSibling.style.marginLeft = "0px"
}

next1.setAttribute('onclick', 'slide_next(this)')
next2.setAttribute('onclick', 'slide_next(this)')
back1.setAttribute('onclick', 'slide_back(this)')
back2.setAttribute('onclick', 'slide_back(this)')

