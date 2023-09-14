function renderManageCourts(court) {

    let courtContainer = document.querySelector(manageCourtContainerId);
    let alertContainer = document.querySelector(alertContainerId);

    let titleContainer = document.createElement('h5');
    titleContainer.innerHTML = `Update: ${court.court_name}`;
    courtContainer.append(titleContainer);

    // Court name container
    let courtNameContainer = document.createElement("div");
    courtNameContainer.className = "mb-3 row";

    // Court name lable element
    let courtNameLabelelement = document.createElement("label");
    courtNameLabelelement.className = "col-sm-4 col-form-label";
    courtNameLabelelement.innerHTML = "Court Name";

    // Court name input container
    let courtNameInputContainer = document.createElement("div");
    courtNameInputContainer.className = "col-sm-8";

    // Court name input element
    let courtNameInputElement = document.createElement("input");
    courtNameInputElement.className = "form-control";
    courtNameInputElement.type = "text";
    courtNameInputElement.name = "court_name";
    courtNameInputElement.value = court.court_name;

    courtNameInputContainer.append(courtNameInputElement);
    courtNameContainer.append(courtNameLabelelement, courtNameInputContainer);
    courtContainer.append(courtNameContainer);

    // Court open time container
    let courtOpenTimeContainer = document.createElement('div');
    courtOpenTimeContainer.className = "mb-3 row";

    // Court open time lable element
    let courtOpenTimeLableElement = document.createElement("label");
    courtOpenTimeLableElement.className = "col-sm-4 col-form-label";
    courtOpenTimeLableElement.innerHTML = "Open Time";

    // Court open time input container
    let courtOpenTimeInputContainer = document.createElement("div");
    courtOpenTimeInputContainer.className = "col-sm-8";

    // Court open time input element
    let courtOpenTimeInputElement = document.createElement("input");
    courtOpenTimeInputElement.className = "form-control";
    courtOpenTimeInputElement.type = "text";
    courtOpenTimeInputElement.name = "court_name";
    courtOpenTimeInputElement.value = court.open_time;

    courtOpenTimeInputContainer.append(courtOpenTimeInputElement);
    courtOpenTimeContainer.append(courtOpenTimeLableElement, courtOpenTimeInputContainer);
    courtContainer.append(courtOpenTimeContainer);

    // Court close time container
    let courtCloseTimeContainer = document.createElement('div');
    courtCloseTimeContainer.className = "mb-3 row";

    // Court close time lable element
    let courtCloseTimeLableElement = document.createElement("label");
    courtCloseTimeLableElement.className = "col-sm-4 col-form-label";
    courtCloseTimeLableElement.innerHTML = "Close Time";

    // Court close time input container
    let courtCloseTimeInputContainer = document.createElement("div");
    courtCloseTimeInputContainer.className = "col-sm-8";

    // Court close time input element
    let courtCloseTimeInputElement = document.createElement("input");
    courtCloseTimeInputElement.className = "form-control";
    courtCloseTimeInputElement.type = "text";
    courtCloseTimeInputElement.name = "court_name";
    courtCloseTimeInputElement.value = court.close_time;

    courtCloseTimeInputContainer.append(courtCloseTimeInputElement);
    courtCloseTimeContainer.append(courtCloseTimeLableElement, courtCloseTimeInputContainer);
    courtContainer.append(courtCloseTimeContainer);

    // Submit button container
    let submitButtonContainer = document.createElement("div");
    submitButtonContainer.className = "col-sm-12 text-center";

    // Submit button
    buttonSubmitElement = document.createElement("button");
    buttonSubmitElement.type = "submit";
    buttonSubmitElement.className = "btn btn-primary";
    buttonSubmitElement.innerHTML = "Update";

    // Submit button onlick
    buttonSubmitElement.addEventListener("click", () => {

        let update = {};
        let payload = {};

        update['name'] = courtNameInputElement.value;
        update['open_time'] = courtOpenTimeInputElement.value;
        update['close_time'] = courtCloseTimeInputElement.value;

        if (update['name']!=court.court_name) {
            payload['court_name']=update['name'];
        }
        if (update['open_time']!=court.open_time) {
            payload['open_time']=update['open_time'];
        }

        if (update['close_time']!=court.close_time) {
            payload['close_time']=update['close_time'];
        }

        console.log(payload);

    });

    submitButtonContainer.append(buttonSubmitElement);
    courtContainer.append(submitButtonContainer);

}
