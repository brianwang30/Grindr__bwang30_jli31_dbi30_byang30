
const answers = document.querySelectorAll('.answer-choice');
const submit = document.querySelector('.submit');

/* mechanism for clicking an answer choice and holding it */
answers.forEach(answer => {
    answer.addEventListener('click', function() {
        /* removes chosen class from every 
        choice and gives the clicked one it*/
        answers.forEach(a => a.classList.remove('chosen'))
        this.classList.add('chosen');
        /* turns gray submit intro green*/
        if (submit.disabled) submit.disabled = false;
        /* changes formaction of the submit button to correct route */
        const routeStart = submit.classList[1];
        if (this.classList.contains('correct')) {
            submit.formAction = `/${routeStart}correct`;
        } else {
            submit.formAction = `/${routeStart}incorrect`;
        }

        /* adds pressed class to have the click effect */
        answer.classList.add('pressed');    
    })
})
answers.forEach(answer => {
    answer.addEventListener('transitionend', function(){
        this.classList.remove('pressed');
    })
})

const body = document.querySelector('body');
const banner = document.querySelector('.banner');

if (banner != null) {
    /* adds a class depending on if the answer is wrong or correct */
    if (banner.textContent.includes('Correct')) {
        banner.classList.add('green-text');
    } else if (banner.textContent.includes('Wrong')) {
        banner.classList.add('red-text');
    } else {
        banner.classList.add('no-text');
    }

    /* if the the answer is correct or wrong, then it does the banner 
    animation*/
    if (!banner.classList.contains('no-text')) {
        body.onload = function() {
            banner.classList.add('appear');
        }
    }
}