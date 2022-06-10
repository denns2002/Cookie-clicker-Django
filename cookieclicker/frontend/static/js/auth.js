$(document).ready(function() {
	$('body').on('click', '.password-control', function(){
		if ($("input[name~='password']").attr('type') == 'password'){
			$(this).addClass('view');
			$("input[name~='password']").attr('type', 'text');
		} else {
			$(this).removeClass('view');
			$("input[name~='password']").attr('type', 'password');
		}
		return false;
	});
});
window.onload=( )=>{
    var password = document.getElementById('id_password');
	const username = document.getElementById('id_username');
    var diff = document.getElementById("diff");
    var nonnumeric = document.getElementById("non-numeric");
    var numeric = document.getElementById("numeric");
	var length = document.getElementById("length");

    password.onfocus = function() {
        document.getElementById("validate").style.height = "105px";
    };

	password.onkeyup = function() {
		// Validate numbers
		var numbers = /[0-9]/g;
		if(password.value.match(numbers)) {
			numeric.classList.add("valid");
			numeric.children[0].classList.remove("fa-xmark");
			numeric.children[0].classList.add("fa-check");
		} else {
			numeric.classList.remove("valid");
			numeric.children[0].classList.add("fa-xmark");
			numeric.children[0].classList.remove("fa-check");
		}
		// non-nums
		var notnumbers = /[^0-9]/g;
		if(password.value.match(notnumbers)) {
			nonnumeric.classList.add("valid");
			nonnumeric.children[0].classList.remove("fa-xmark");
			nonnumeric.children[0].classList.add("fa-check");
		} else {
			nonnumeric.classList.remove("valid");
			nonnumeric.children[0].classList.add("fa-xmark");
			nonnumeric.children[0].classList.remove("fa-check");
		}
		// lenght
		if(password.value.length >= 8) {
			length.classList.add("valid");
			length.children[0].classList.remove("fa-xmark");
			length.children[0].classList.add("fa-check");
		} else {
			length.classList.remove("valid");
			length.children[0].classList.add("fa-xmark");
			length.children[0].classList.remove("fa-check");
		}
		// difference
		if(password.value.toString().includes(username.value)) {
			diff.classList.remove("valid");
			diff.children[0].classList.add("fa-xmark");
			diff.children[0].classList.remove("fa-check");
		} else {
			diff.classList.add("valid");
			diff.children[0].classList.remove("fa-xmark");
			diff.children[0].classList.add("fa-check");
		}
	};
}