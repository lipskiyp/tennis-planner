async function sessionsGET(startDate='', endDate='') {

    const response = await fetch(`/api/sessions?start_date=${startDate}&end_date=${endDate}`, {
        method: "GET",
    });
    return await response.json();

}