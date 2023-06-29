var title = document.getElementById('title');
var title_output = document.getElementById('title_output');

title_output.textContent = title.value;
title.addEventListener('input', function () {
	title_output.textContent = title.value;
});

var date = document.getElementById('date');
var date_output = document.getElementById('date_output');

date_output.textContent = date.value;
date.addEventListener('input', function () {
	date_output.textContent = date.value;
});

var content = document.getElementById('content');
var content_output = document.getElementById('content_output');

content_output.innerHTML = content.value;
content.addEventListener('input', function () {
	content_output.innerHTML = content.value;
});

var button = document.getElementById('call_to_action_button');
var button_output = document.getElementById('button_output');

if (button.value == "") {
	button_output.style.display = "none"
} else {
	button_output.style.display = "block"
}
button_output.innerText = button.value;
button.addEventListener('input', function () {
	if (button.value == "") {
		button_output.style.display = "none"
	} else {
		button_output.style.display = "block"
	}
	button_output.innerText = button.value;
});

var button_link = document.getElementById('call_to_action_link');

button_output.href = button_link.value;
button_link.addEventListener('input', function () {
	button_output.href = button_link.value;
});

var image_url = document.getElementById('image_url')
var image_output = document.getElementById('image_output');

image_output.src = image_url.value;
image_url.addEventListener('input', function () {
	image_output.src = image_url.value;
});
