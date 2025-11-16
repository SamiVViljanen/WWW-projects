const container = document.querySelector('.container');

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('SignUpLink')) {
         e.preventDefault();
         container.classList.add('active');
     }
     
     if (e.target.classList.contains('SignInLink')) {
         e.preventDefault();
         container.classList.remove('active');
     }
});