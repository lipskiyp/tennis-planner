function renderAddSessionFormElement() {

    let addSessionFormContainer = $(addSessionFormContainerId);

    // Alert
    let alertContainer = document.querySelector(alertContainerId);

    // Client container
    let clientContainer = document.createElement("div");
    clientContainer.className = "mb-3 row";

    // Client select lable
    let clientSelectLabel = document.createElement("label");
    clientSelectLabel.className = "col-sm-2 col-form-label";
    clientSelectLabel.innerHTML = "Client";

    // Client select container
    let clientSelectContainer = document.createElement("div");
    clientSelectContainer.className = "col-sm-10";

    // Client select element
    let clientSelectElement = document.createElement("select");
    clientSelectElement.className = "form-select";
    clientSelectElement.name = "client";
    usersListGET(is_client=true, is_coach='', is_staff='')
    .then(clients => {
        clients.forEach(client => {
            // Create option element
            let clientOptionElement = document.createElement("option");
            clientOptionElement.value = client.id;
            clientOptionElement.innerHTML = client.email;
            // Add option element to select element
            clientSelectElement.append(clientOptionElement);
        });
    });

    clientSelectContainer.append(clientSelectElement);
    clientContainer.append(clientSelectLabel, clientSelectContainer);
    addSessionFormContainer.append(clientContainer);

    // Coach container
    let coachContainer = document.createElement("div");
    coachContainer.className = "mb-3 row";

    // Coach select lable
    let coachSelectLabel = document.createElement("label");
    coachSelectLabel.className = "col-sm-2 col-form-label";
    coachSelectLabel.innerHTML = "Coach";

    // Coach select container
    let coachSelectContainer = document.createElement("div");
    coachSelectContainer.className = "col-sm-10";

    // Coach select element
    let coachSelectElement = document.createElement("select");
    coachSelectElement.className = "form-select";
    coachSelectElement.name = "coach";

    // Coach empty option
    let coachNoneOptionElement = document.createElement("option");
    coachNoneOptionElement.value = "";
    coachNoneOptionElement.innerHTML = "None";
    coachSelectElement.append(coachNoneOptionElement);

    usersListGET(is_client='', is_coach=true, is_staff='')
    .then(coaches => {
        coaches.forEach(coach => {
            // Create option element
            let coachOptionElement = document.createElement("option");
            coachOptionElement.value = coach.id;
            coachOptionElement.innerHTML = coach.email;
            // Add option element to select element
            coachSelectElement.append(coachOptionElement);
        });
    });

    coachSelectContainer.append(coachSelectElement);
    coachContainer.append(coachSelectLabel, coachSelectContainer);
    addSessionFormContainer.append(coachContainer);

    // Court container
    let courtContainer = document.createElement("div");
    courtContainer.className = "mb-3 row";

    // Court select lable
    let courtSelectLabel = document.createElement("label");
    courtSelectLabel.className = "col-sm-2 col-form-label";
    courtSelectLabel.innerHTML = "Court";

    // Court select container
    let courtSelectContainer = document.createElement("div");
    courtSelectContainer.className = "col-sm-10";

    // Courts select element
    let courtSelectElement = document.createElement("select");
    courtSelectElement.className = "form-select";
    courtSelectElement.name = "court";
    courtsGET()
    .then(courts => {
        courts.forEach(court => {
            // Create option element
            let courtOptionElement = document.createElement("option");
            courtOptionElement.value = court.id;
            courtOptionElement.innerHTML = court.court_name;
            // Add option element to select element
            courtSelectElement.append(courtOptionElement);
        });
    });

    courtSelectContainer.append(courtSelectElement);
    courtContainer.append(courtSelectLabel, courtSelectContainer);
    addSessionFormContainer.append(courtContainer);

    // Date container
    let dateContainer = document.createElement("div");
    dateContainer.className = "mb-3 row";

    // Date input lable
    let dateInputLabel = document.createElement("label");
    dateInputLabel.className = "col-sm-2 col-form-label";
    dateInputLabel.innerHTML = "Date";

    // Date input container
    let dateInputContainer = document.createElement("div");
    dateInputContainer.className = "col-sm-10";

    // Date input element
    dateInputElement = document.createElement("input");
    dateInputElement.name = "date";
    dateInputElement.type = "date";

    dateInputContainer.append(dateInputElement);
    dateContainer.append(dateInputLabel, dateInputContainer);
    addSessionFormContainer.append(dateContainer);

    // Time container
    let timeContainer = document.createElement("div");
    timeContainer.className = "mb-3 row";

    // Time input lable
    let timeInputLabel = document.createElement("label");
    timeInputLabel.className = "col-sm-2 col-form-label";
    timeInputLabel.innerHTML = "Time";

    // Time input container
    let timeInputContainer = document.createElement("div");
    timeInputContainer.className = "col-sm-10";

    // Time input element
    timeInputElement = document.createElement("input");
    timeInputElement.name = "time";
    timeInputElement.type = "time";

    timeInputContainer.append(timeInputElement);
    timeContainer.append(timeInputLabel, timeInputContainer);
    addSessionFormContainer.append(timeContainer);

    // Submit button container
    let submitButtonContainer = document.createElement("div");
    submitButtonContainer.className = "col-sm-12 text-center";

    // Submit button
    buttonSubmitElement = document.createElement("button");
    buttonSubmitElement.type = "submit";
    buttonSubmitElement.className = "btn btn-primary";
    buttonSubmitElement.innerHTML = "Add Session";

    // Submit button onlick
    buttonSubmitElement.addEventListener("click", () => {
        let client = clientSelectElement.value;
        let coach = coachSelectElement.value;
        let court = courtSelectElement.value;
        let date = dateInputElement.value;
        let time = timeInputElement.value;
        addSessionPOST(client=client, coach=coach, court=court, date=date, time=time)
        .then(response => {
            if (response.ok) {
                alertContainer.style.display = "block";
                alertContainer.className = "alert alert-success";
                alertContainer.innerHTML = "Session added successfully.";
            } else {
                alertContainer.style.display = "block";
                alertContainer.className = "alert alert-warning";
                alertContainer.innerHTML = "Failed to add session.";
            }
        });
    });

    submitButtonContainer.append(buttonSubmitElement);
    addSessionFormContainer.append(submitButtonContainer);

}