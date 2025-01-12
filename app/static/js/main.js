//Switch between questions during a quiz
function toggleQuestion(hide, show) {
    var divToHide = document.getElementById(hide);
    var divToShow = document.getElementById(show);

    divToHide.style.display = 'none';
    divToShow.style.display = 'block';
}


//Set year for footer copyright
window.addEventListener('load', () => {
    const currentYear = new Date().getFullYear()
    document.getElementById('currentYear').textContent = currentYear
});

//Show flashed messages aka notification toasts
const toastElList = document.querySelectorAll('.toast');
const options = {
    delay: 4000
}
const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, options));

window.addEventListener('load', () => {
    for (let toast of toastList) {
        toast.show();
    }
});