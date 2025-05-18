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
})