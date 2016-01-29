$(document).ready(function() {
	//listen for click
	$('form.vote').on('submit', function(e){
		e.preventDefault();
		var el = $(this);

        var ctype = el.find('input[name=content_type]').val()
            object_id = el.find('input[name=object_id]').val()
            vote = el.find('input[name=vote]').val()
			url = el.attr('action'),

            console.log(url, "ct:", ctype, "object_id:", object_id, "vote:", vote);
		$.ajax({
	            type:'POST',
		        url: url,
		        data: {
	                'content_type': ctype,
	                'object_id': object_id,
	                'vote': vote,
                },
				dataType: "json",
		        success : function(data) {
		        	console.log("Voted");
		        	var id = object_id;
                    $("p."+ctype+"-"+id).text(data['score'].score);
                }
	    });
	});
    // Search Jaryanaks
    $('#search').keyup(function(e){
        e.preventDefault();
        var search_el = $(this);

        $.ajax({
            type: "POST",
            url: "/search/",
            data: {
                'search_text': $('#search').val(),
            },
            dataType: 'html',
            success:function(data, textStatus){
                $('#search-results').html(data);
            }
        });
    });

    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
});
