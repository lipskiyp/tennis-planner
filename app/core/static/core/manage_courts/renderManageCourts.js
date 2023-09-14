function renderCourts() {

    let courtsContainer = document.querySelector(manageCourtsContainerId);

    courtsGET()
    .then(courts => {

        let n_col = 4; // NB must be multiple of 12
        let n_current = 0;
        let rowElement;

        courts.forEach(court => {
            if (n_current%n_col==0) {
                // Append current row element
                if (n_current>0) {
                    courtsContainer.append(rowElement);
                }
                // Create new row element
                rowElement = document.createElement('div');
                rowElement.className = 'row mt-3';
            }
            // Create column element
            let colElement = document.createElement('div');
            colElement.className = `col-${12/n_col} d-flex justify-content-center`;

            // Create card element
            let cardElement = document.createElement('div');
            cardElement.className = 'card';
            cardElement.addEventListener('click', () => {
                courtsContainer.style.display = "none";
                renderManageCourts(court);
            });

            // Create card body element
            let cardBodyElement = document.createElement('div');
            cardBodyElement.className = 'card-body';

            // Create card title element
            let cardTitleElement = document.createElement('h6');
            cardTitleElement.className = 'card-title text-center';
            cardTitleElement.innerHTML = court.court_name;

            // Create image element
            let cardImageElement = document.createElement('img');
            cardImageElement.src = courtImageUrl;
            cardImageElement.width = 150;

            cardBodyElement.append(cardTitleElement, cardImageElement);
            cardElement.append(cardBodyElement);
            colElement.append(cardElement);
            rowElement.append(colElement);

            n_current++;
        });
        courtsContainer.append(rowElement);
    });

}