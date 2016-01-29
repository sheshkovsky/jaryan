$(document).ready(function() {
	//listen for click
	$('form.vote').on('submit', function(e){
		e.preventDefault();
		var vote_el = $(this);
		var
			url = vote_el.attr('action'),
			model = vote_el.attr('model'),
			direction = vote_el.attr('direction'),
			object_id = vote_el.attr('id'),
			allow_xmlhttprequest = "True" ;
            console.log(allow_xmlhttprequest, url, model, direction, object_id);
		$.ajax({
	            type:'POST',
		        url: vote_el.attr('action'),
		        data: {
	                'model': model,
	                'object_id': object_id,
	                'direction': direction,
                },
				dataType: "json",
		        success : function(data) {
		        	console.log("Voted");
		        	var pk = object_id;
                    $("p."+model+"-"+pk).text(data['score'].score);
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
