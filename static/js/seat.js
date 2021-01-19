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

function get_class(e) {
    var e = e || window.event;
    var elem = e.target || e.srcElement;
    var elem_id = elem.id;
    var filename = document.getElementsByTagName("map")[0].id;
    var seat = "{{seat}}";
    if (seat != elem_id) {
        var form = document.createElement("form");
        var input = document.createElement("input");
        var scroll = document.createElement("input");
        scroll.name = "scroll";
        scroll.type = "hidden";
        scroll.value = document.documentElement.scrollTop;
        form.appendChild(scroll);
        form.action = "/find/" + elem.id;
        form.method = "post";
        input.name = "filename";
        input.type = "hidden";
        input.value = filename;
        form.appendChild(input);
        document.body.appendChild(form);

        form.submit();

    }


}

function submit(e) {
    var elem = document.getElementById("seat");
    if (elem != null) {
        elem.parentNode.removeChild(elem);
    }
    var form = document.getElementById("submit");
    var e = e || window.event;

    var elem = e.target || e.srcElement;

    var elem_id = elem.id;
    var input = document.createElement("input");
    var input2 = document.createElement("input");
    var msg = document.getElementById("submit_msg");
    var filename = document.getElementsByTagName("map")[0].id;
    input.name = "filename"
    input.value = filename
    input.type = "hidden";
    form.appendChild(input)


    input2.type = "hidden";

    input2.name = "seat";

    input2.value = filename + " " + elem.id;

    input2.id = "seat";
    msg.textContent = elem.id + "を選択しました";

    form.appendChild(input2);


}

function flag_check() {
    var checkbox = document.getElementById("flag");
    var input = document.createElement("input");
    var form = document.getElementById("submit");
    input.name = "flag"
    input.type = "hidden"
    if (checkbox.checked == true) {
        input.value = "on";
    } else {
        input.value = "off";
    }
    form.appendChild(input)
}