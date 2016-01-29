jQuery(document).ready(function($) 
    {
    function show_reply_form(event) {
        var $this = $(this);
        var comment_id = $this.data('comment-id');

        $('#id_parent').val(comment_id);
        $('#form-comment').insertAfter($this.closest('.comment'));
    };

    function cancel_reply_form(event) {
        $('#id_comment').val('');
        $('#id_parent').val('');
        $('#form-comment').appendTo($('#wrap_write_comment'));
    }

    $.fn.ready(function() {
        $('.comment_reply_link').click(show_reply_form);
        $('#cancel_reply').click(cancel_reply_form);
    });
});
