var modalBtn = document.querySelector('.add-password-btn');
var modalBg = document.querySelector('.modal-bg');
var modalClose = document.querySelector('.modal-close');

modalBtn.addEventListener('click', function(){
    modalBg.classList.add('modal-bg-active');
});

modalClose.addEventListener('click', function(){
    modalBg.classList.remove('modal-bg-active');
});