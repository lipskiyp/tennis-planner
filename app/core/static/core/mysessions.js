$(document).ready(() => {
    // $("#SessionsContainer").html("Hello");
    renderMySessions();
});

function renderMySessions() {

    sessionsGET()
    .then(sessions => {
        const sessionsContainer = $("#SessionsContainer");
        sessions.forEach(session => {  // For every session
            sessionsContainer.append(createSessionElement(session))
        });
    });

}

function createSessionElement(session) {

    console.log(session)

    let sessionElement = document.createElement("div");
    sessionElement.className = "card";

    let sessionBody = document.createElement("div");
    sessionBody.className = "card-body";

    let sessionTittle = document.createElement("h5");
    sessionTittle.className = "card-title";
    sessionTittle.innerHTML = session.court.court_name;

    let sessionSubtitle = document.createElement("h6");
    sessionSubtitle.className = "card-subtitle mb-2 text-body-secondary";
    sessionSubtitle.innerHTML = `On ${session.session_date} at ${session.session_time}`;

    sessionBody.append(sessionTittle, sessionSubtitle);
    sessionElement.append(sessionBody);

    return sessionElement;

}