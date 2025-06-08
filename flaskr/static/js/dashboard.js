$(document).ready(function () {
    $('#delete-oldest').click(function (e) {
        e.preventDefault();
        const url = $(this).data('url');

        $.ajax({
            url: url,
            type: 'POST',
        })
            .done(function (response) {
                alert(response.message || 'Record deleted.');
                updateTable();
            })
            .fail(function (xhr) {
                const errorMsg = xhr.responseJSON?.error || 'Unknown error occurred.';
                alert(errorMsg);
            });
    });

    function updateTable() {
        const rawRowCount = $('#row-count').val();
        const rowCount = parseInt(rawRowCount, 10);

        if (isNaN(rowCount) || rowCount < 1 || rowCount > 100) {
            alert('Please enter a valid number between 1 and 100.');
            return;
        }

        $.ajax({
            url: '/update_table',
            type: 'GET',
            data: {count: rowCount},
            success: function (data) {
                $('#table').html(data);
            },
            error: function () {
                alert('Error updating the table.');
            }
        });
    }

    $('#update-table').click(function (e) {
        e.preventDefault();
        updateTable();
    });


    function fetchStatus() {
        fetch("/api/status")
            .then(res => res.json())
            .then(data => {
                if ("led" in data) {
                    const ledStatusEl = document.getElementById("led-status");
                    ledStatusEl.textContent = data.led ? "ON" : "OFF";
                    ledStatusEl.className = "badge " + (data.led ? "bg-success" : "bg-danger");
                }
                if ("measurement" in data) {
                    const measurementStatusEl = document.getElementById("measurement-status");
                    measurementStatusEl.textContent = data.measurement ? "ON" : "OFF";
                    measurementStatusEl.className = "badge " + (data.measurement ? "bg-success" : "bg-danger");
                }
                if ("interval" in data) {
                    document.getElementById("interval-value").innerText = data.interval;
                }
            });
    }

    function toggleMeasurement(on) {
        const url = on ? "/api/turn_on_measurements" : "/api/turn_off_measurements";
        fetch(url, {method: "POST"})
            .then(() => fetchStatus())
            .catch(() => alert("Failed to change measurement state"));
    }

    function toggleLED(on) {
        const url = on ? "/api/turn_on_led" : "/api/turn_off_led";
        fetch(url, {method: "POST"})
            .then(() => fetchStatus())
            .catch(() => alert("Failed to change LED state"));
    }

    function setIntervalValue(value) {
        const interval = parseInt(value);
        if (isNaN(interval) || interval < 1 || interval > 3600) {
            alert("Please enter a valid interval between 1 and 3600 seconds.");
            return;
        }

        fetch("/api/set_measurements_interval", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({interval: interval})
        })
            .then(res => {
                if (!res.ok) return res.json().then(e => {
                    throw new Error(e.error);
                });
                return res.json();
            })
            .then(() => fetchStatus())
            .catch(err => alert("Error: " + err.message));
    }

    $('#toggle-measurement').click(function (e) {
        const isOn = $('#measurement-status').text().trim() === 'ON';
        toggleMeasurement(!isOn);
    });
    $('#toggle-led').click(function (e) {
        const isOn = $('#led-status').text().trim() === 'ON';
        toggleLED(!isOn);
    });
    $('#set-interval-button').click(function (e) {
        e.preventDefault();
        const value = $('#interval-input').val();
        setIntervalValue(value);
    });
})