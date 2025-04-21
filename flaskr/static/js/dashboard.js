$(document).ready(function() {
    $('#delete-oldest').click(function(e) {
        e.preventDefault();
        const url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'POST',
            success: function(response) {
                alert('Oldest entry deleted successfully.');
            },
            error: function(xhr, status, error) {
                alert('Error deleting the oldest entry.');
            }
        });
    });
});