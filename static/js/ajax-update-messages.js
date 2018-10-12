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
    $.ajax({
        type: 'POST',
        url: window.location.protocol + "//" + window.location.host + '/ajax_update_messages/',
        processData: false,
        success: function(context) {
          if (context.none != true){
           $('.fa-envelope').css('color', 'red');
           for (i = 0; i < Object.keys(context).length; i++){
             if (context[i].chatlist){
               chat = $('.chatlist').find("[name = "+context[i].id+"]");
               if (context[i].text){
                 chat.find('.facial').html("<img class='round-im-25' src='"+context[i].ava+"' style='vertical-align: middle;'>"+context[i].text+"");
               }
               else{
                 chat.find('.facial').html("<img class='round-im-25' src='"+context[i].ava+"' style='vertical-align: middle;'>Images");
               }
               chat.find('.facial').css('background-color', "rgb(247, 245, 245)");
             }
             if (i == 0){
                $('.first-column').append("<div class='alert alert-primary new-message' style='bottom: 10px;' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close' id='currentalert'><span aria-hidden='true'>&times;</span></button></div>");
                }
             else if (i<14){
               $('.first-column').append("<div class='alert alert-primary new-message' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close' id='currentalert'><span aria-hidden='true'>&times;</span></button></div>");
               bottom = 10 + i*60;
               $('#currentalert').parent().css('bottom', bottom);
             }
               if (context[i].chat){
                 if (context[i].num >1){
                   $('#currentalert').before(context[i].num + " new messages in chat: "+ context[i].name)
                 }
                 else if (context[i].num ==1){
                   $('#currentalert').before("1 new message in chat: "+ context[i].name)
                 }
               }
               else {
                 if (context[i].num >1){
                   $('#currentalert').before(context[i].f_n+" "+context[i].l_n+ " sent you "+context[i].num+" messages")
                 }
                 else if (context[i].num ==1){
                   $('#currentalert').before(context[i].f_n+" "+context[i].l_n+ " sent you a message")
                 }
               }
               $('#currentalert').removeAttr("id");
             }
             $('.new-message').delay(10000).fadeOut("slow");
           }

        },
    });
    return false;
}, 0.3*60*1000);
