async function sessionsGET(startDate='', endDate='', court='') {

    const response = await fetch(`/api/sessions?start_date=${startDate}&end_date=${endDate}&court=${court}`, {
        method: "GET",
    });
    return await response.json();

}