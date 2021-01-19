scroll();
var form = document.getElementById("submit");

var parent_username = window.parent.document.getElementById("username");

var username = parent_username.textContent;
var name_input = document.createElement("input");

name_input.type = "hidden";

name_input.name = "name";

name_input.value = username;

form.appendChild(name_input);

function scroll() {
    try {
        s = "{{scr}}";
        if (s != "") {
            document.documentElement.scrollTop = Number(s);
        }


    } catch (error) {
        alert(error);
    }
}