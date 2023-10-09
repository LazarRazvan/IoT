/*
 * Application state change function.
 *
 * If application is turned on, the application config div should become
 * read-only alongside with all associated fields.
 *
 * If application is turned off, application config should be editable.
 */

function appSetState() {
	// Get variables
	var dataCont = document.getElementById('data');
	var appState = document.getElementById("checkbox");
	var appConfigActivePower = document.getElementById('app-config-active-power');

	// Validate application config active power is not empty
	if (appConfigActivePower.value.trim() === "") {
		alert("Error! Please select a value for active power!");
		appState.checked = false;
		return; // Stop further execution
	}

	// Validate application config active power is valie
	var floatPattern = /^[-+]?[0-9]*\.?[0-9]+$/;
	if (!floatPattern.test((appConfigActivePower.value.trim()))) {
		alert("Error! Please select a valid value for active power (ex: 2.5)!");
		appState.checked = false;
		return; // Stop further execution
	}

	console.log("Call post")
	// TODO: Send post to server
	var xhr = new XMLHttpRequest();
	//xhr.open("POST", "/app_state_change", true);
	xhr.open("POST", "/app_state_change", false); //synchronous request
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhr.send(JSON.stringify({ "app_state": appState.checked, "app_config_trigger_value": appConfigActivePower.value }));

	console.log("Force reset")
	location.reload()
}

/*
 * Should be executed when DOM is loaded so all elements are available and
 * update application status information based on server response.
 */
document.addEventListener('DOMContentLoaded', function() {
	var checkbox = document.getElementById('checkbox');
	var dataCont = document.getElementById('data');
	var appConfigActivePower = document.getElementById('app-config-active-power');

	if (checkbox.checked) {
		appConfigActivePower.readOnly = true;
		dataCont.style.display = 'block'; // Show the div
	} else {
		appConfigActivePower.readOnly = false;
		dataCont.style.display = 'none'; // Hide the div
	}
});
