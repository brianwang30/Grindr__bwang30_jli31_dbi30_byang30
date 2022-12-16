/* adds sticky class to the navbar when user scrolls */
window.addEventListener("scroll", function(){
    const nav = document.querySelector('nav');
    console.log(nav);
    nav.classList.toggle('sticky', window.scrollY > 0);
    })

    