async function sessionsGET(startDate='', endDate='', court='', start_time_before='', start_time_after='') {

    const response = await fetch(`/api/sessions?start_date=${startDate}&end_date=${endDate}&court=${court}&start_time_before=${start_time_before}&start_time_after=${start_time_after}`, {
        method: "GET",
    });
    return await response.json();

}

async function usersListGET(is_client='', is_coach='', is_staff='') {

    const response = await fetch(`/api/user/list?is_client=${is_client}&is_coach=${is_coach}&is_staff=${is_staff}`, {
        method: "GET",
    });
    return await response.json();

}

async function courtsGET() {

    const response = await fetch(`/api/courts`, {
        method: "GET",
    });
    return await response.json();

}

async function addSessionPOST(client, coach, court, date, time) {

    // https://docs.djangoproject.com/en/3.2/ref/csrf/
    let csrftoken = getCookie('csrftoken');

    let payload = {
        "client_id": parseInt(client),
        "court_id": parseInt(court),
        "session_date": date,
        "session_time": time,
    }

    if(coach) {
        payload["coach_id"] = parseInt(coach);
    }

    const response = await fetch("/api/sessions/", {
        method: "POST",
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json', 'accept': 'application/json'},
        body: JSON.stringify(payload)
    });
    return response;

}