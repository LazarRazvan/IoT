function genericAction() {
	var stateAction;
	var xhr = new XMLHttpRequest();
    var button = event.target;
	var buttonId = button.id;

	// Decide if turn on or turn off the switch
	console.log("Button clicked: " + buttonId)
	//
	if (button.style.backgroundColor === "rgb(246, 246, 222)") {
		console.log(genericAction.name + " turn off");
		stateAction = "off";
		button.style.backgroundColor = "#4d4d4d";
	} else if (button.style.backgroundColor === "rgb(77, 77, 77)") {
		console.log(genericAction.name + " turn on");
		stateAction = "on";
		button.style.backgroundColor = "#f6f6de";
	} else {
		alert("Error! Unknown state!");
		return;
	}

	xhr.open("POST", "/set_button", false); //synchronous request
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhr.send(JSON.stringify({ "name" : buttonId, "state": stateAction }));
}

/*
 * Should be executed when DOM is loaded so all elements are available and
 * update buttons based on current lights state.
 */
document.addEventListener("DOMContentLoaded", function () {
	console.log("Get buttons!");
	//
    var hol = document.getElementById("hol");
    var baie1 = document.getElementById("baie1");
    var baie2 = document.getElementById("baie2");
    var living = document.getElementById("living");
    var bucatarie = document.getElementById("bucatarie");

    // Fetch data from the server on page load.
    fetch('/get_button')
        .then(response => response.json())
        .then(data => {
			console.log(data)
            // living
            if (data["living"] === true) {
                living.style.backgroundColor = "#f6f6de";
            } else {
                living.style.backgroundColor = "#4d4d4d";
            }
            // bucatarie
            if (data["bucatarie"] === true) {
                bucatarie.style.backgroundColor = "#f6f6de";
            } else {
                bucatarie.style.backgroundColor = "#4d4d4d";
            }
            // hol
            if (data["hol"] === true) {
                hol.style.backgroundColor = "#f6f6de";
            } else {
                hol.style.backgroundColor = "#4d4d4d";
            }
            // baie1
            if (data["baie1"] === true) {
                baie1.style.backgroundColor = "#f6f6de";
            } else {
                baie1.style.backgroundColor = "#4d4d4d";
            }
            // baie2
            if (data["baie2"] === true) {
                baie2.style.backgroundColor = "#f6f6de";
            } else {
                baie2.style.backgroundColor = "#4d4d4d";
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

