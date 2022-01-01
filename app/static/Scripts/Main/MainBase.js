const pro_btn = document.querySelector('#pro_btn')
const pro_menu = document.querySelector('.profile_menu')

pro_btn.addEventListener('click', ()=>{
    if (pro_menu.hasAttribute('id', 'show_pro_menu')){
        pro_menu.removeAttribute('id', 'show_pro_menu')
    }else{
        pro_menu.setAttribute('id', 'show_pro_menu')
    }
})