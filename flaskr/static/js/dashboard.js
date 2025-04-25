$(document).ready(function () {
    $('#delete-oldest').click(function (e) {
        e.preventDefault();
        const url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'POST',
            success: function (response) {
                if (response.success) {
                    updateTable();
                } else {
                    alert('Something went wrong.');
                }
            },
            error: function () {
                alert('Error deleting the oldest entry.');
            }
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