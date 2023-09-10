$(document).ready(() => {

    renderUpcomingSessions("#SessionsContainer", "#SessionsArchieveButton");

});

function renderUpcomingSessions(sessionsContainerId, SessionsArchieveButtonId) {

    renderSessions(sessionsContainerId, startDate=getToday(), endDate="");

    $(SessionsArchieveButtonId).html("Archieve")
    $(SessionsArchieveButtonId).off('click').on('click', function() {
        renderArchieveSessions(sessionsContainerId, SessionsArchieveButtonId);
    });

}

function renderArchieveSessions(sessionsContainerId, SessionsArchieveButtonId) {

    renderSessions(sessionsContainerId, startDate="", endDate=getToday());

    $(SessionsArchieveButtonId).html("Upcoming")
    $(SessionsArchieveButtonId).off('click').on('click', function() {
        renderUpcomingSessions(sessionsContainerId, SessionsArchieveButtonId);
    });

}

function renderSessions(sessionsContainerId, startDate="", endDate="") {

    let sessionsContainer = $(sessionsContainerId);
    sessionsContainer.empty();  // clear container

    sessionsGET(startDate=startDate, endDate=endDate)
    .then(sessions => {
        sessions.forEach(session => {  // For every session
            sessionsContainer.append(createSessionElement(session))
        });
    });

};

function getToday() {

    const date = new Date();
    return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,"0")}-${String(date.getDate()).padStart(2, '0')}`;

};