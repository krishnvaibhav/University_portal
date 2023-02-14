const error = document.querySelector('.flashing-error');

if(error.textContent != ""){
    error.classList.remove('hidden')
    setTimeout(flashing,2000)
}


function flashing() {
    error.classList.add('hidden')
  }




