window_width = window.innerWidth

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
    // pic_name.innerHTML = file.value.slice(12)
}
file.addEventListener('change', import_image, false)

