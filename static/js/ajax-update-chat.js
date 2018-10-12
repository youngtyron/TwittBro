function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
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
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


setInterval(function(){
    last = $('#message-list').find('.list-group-item').last().attr('name');
    $.ajax({
        type: 'POST',
        url: 'ajax_update_chat/',
        data: last,
        processData: false,
        success: function(context) {
          if (context.none != true){
          $('.fa-envelope').css('color', 'red');
           for (i = 0; i < Object.keys(context).length; i++){
             $('#message-list').find('.list-group-item').last().after("<li class='list-group-item "+context[i].wr_id+"' id = 'current' name ='"+context[i].id+"'><p class = 'writer'>" + context[i].f_n + " "+
                                         context[i].l_n + "</p>"+"<p class='date'>"+context[i].date+"</p>" + "</li>");
             if (context[i].text) {$('#current').find('.writer').after("<p>"+context[i].text+"</p>")};
             if (context[i].images){
               $('#current').find('.date').before("<p>" + context[i].images +"</p>");
             }
             if(context[i].grey){
               $('#current').css('background-color', 'rgb(247, 245, 245)');
             }
             else{
               $('#current').css('background-color', 'white');
             }
             $('#current').removeAttr("id");
           }
         }
        },
    });
    return false;
}, 0.3*60*1000);
