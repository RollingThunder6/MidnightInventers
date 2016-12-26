$(document).ready(function() {
	$(".click-dropdown-field").click(function(event) {
		$(this).children('.content').slideToggle(300, function() {
			console.log("Slide event success.")
		})
	});
});