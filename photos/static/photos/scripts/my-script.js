const dropdowns = document.getElementsByClassName("dropdown-btn");

for (let i = 0; i < dropdowns.length; i++) {
    dropdowns[i].addEventListener("click", function() {
        this.classList.toggle("active");
        const dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "block";
        }
    });
}

//Upload modal image display start
function triggerFileInput() {
    document.getElementById('img').click();
}

function displayImage(input) {
    var file = input.files[0];

    if (file) {

        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById('add-new-filename').innerHTML = file.name;
            document.getElementById('uploadedImage').src = e.target.result;
            document.getElementById('click').style.display = "none";
        };

        reader.readAsDataURL(file);
    }
}
//Upload modal image display end

function submitForm(identity){
    const el = document.getElementById(identity)
    if (!el.checked && window.location.href.includes("options") && !window.location.href.includes("&")) {
        window.location.href = "/"
        return;
    }
    document.getElementById("myForm").submit();
}

const modal = document.getElementById("myModal");
const btn = document.getElementById("myBtn");
const span = document.getElementsByClassName("close-upload")[0];
const body = document.getElementsByTagName('body')[0];

btn.onclick = function() {
    modal.style.display = "block";
    body.style.overflow = "hidden";
}

span.onclick = function() {
    modal.style.display = "none";
    body.style.overflow = "auto";
}

const imgModal = document.getElementById("imgModal");
const imgSpan = document.getElementsByClassName("close-photo")[0];

if (window.location.href.includes("photo_")){
    imgModal.style.display = "block";
    body.style.overflow = "hidden";
}


if (imgSpan !== undefined){
    imgSpan.onclick = function() {
        imgModal.style.display = "none";
        body.style.overflow = "auto";
        if (window.location.href.includes("&")){
            tagList = window.location.href.split("&")
            tagList.pop()
            path = tagList.join("&")
        } else {
            path = window.location.origin
        }

        window.location.replace(path)
    }
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        body.style.overflow = "auto";
    }

    if (event.target == imgModal) {
        imgModal.style.display = "none";
        body.style.overflow = "auto";
        if (window.location.href.includes("&")){
            tagList = window.location.href.split("&")
            tagList.pop()
            path = tagList.join("&")
        } else {
            path = window.location.origin
        }

        window.location.replace(path)
    }
}

function submitModalForm(data) {
    const modal_form = document.getElementById("modal-form");

    if (data === "save"){
        const filename = document.getElementById("filename")
        const new_filename = document.getElementById("new-filename")
        filename.value = new_filename.innerText
    }else if (data === "add"){
        if (!window.location.href.includes("options")) {
            modal_form.action = window.location.href + "/options"
        }
        const filename = document.getElementById("add-filename")
        const new_filename = document.getElementById("add-new-filename")
        filename.value = new_filename.innerText
    }
    modal_form.submit()
}