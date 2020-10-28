const input = document.querySelector("input");

input.oninput = enableSubmitButton;

function enableSubmitButton(e) {
    if(e.target.value.length === 0) document.getElementById("login").disabled = true;
    else document.getElementById("login").disabled = false;
}
