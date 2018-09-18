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

$(document).ready(function() {
    $('#messaging').ajaxForm({
      type : 'POST',
      dataType: "json",
      url : 'ajax_message/',
      clearForm : true,
      success: function (context) {
        if (context.too_much){
          alert('You can send no more than 10 images')
        }
        else if (context.images == null && context.text != null){
          $('#message-list').append("<li class = 'list-group-item' style ='background-color: rgb(247, 245, 245);'> <p>" + context.f_name + ' ' + context.l_name + "</p> <p>" + context.text + "</p> <p> Right now </p></li>");
        }
        else if (context.images != null && context.text != null) {
          $('#message-list').append("<li class = 'list-group-item' style ='background-color: rgb(247, 245, 245);'> <p>" + context.f_name + ' ' + context.l_name + "</p> <p>" + context.text + "</p><p>" + context.images + "</p><p> Right now </p></li>");
        }
        else if (context.text == null && context.images != null){
          $('#message-list').append("<li class = 'list-group-item' style ='background-color: rgb(247, 245, 245);'> <p>" + context.f_name + ' ' + context.l_name + "</p><p>" + context.images + "</p><p> Right now </p></li>");
        }
      },
      error: function (error) {
        alert('Error. Try again please!');
      }
    });
});


$('.scroll-message-box').scroll(function() {
  height = $('.scroll-message-box').scrollTop();
  if (height==0){
    number = $('.page-number').attr('name');
    $.ajax({
      data: number,
      type : 'POST',
      url : 'ajax_scroll_messages/',
      processData: false,
      success: function(context){
        page = parseInt($('.page-number').attr('name')) + 1;
        $('.page-number').attr('name', page);
        for (i = 0; i < Object.keys(context).length; i++){
            $('#message-list').prepend("<li class='list-group-item' id = 'current' name ='"+context[i].wr_id+"'><p class = 'writer'>" + context[i].f_n + " "+
                                        context[i].l_n + "</p>"+"<p class='date'>"+context[i].date+"</p>" + "</li>");
            if(context[i].text){$('#current').find('.writer').after("<p>"+context[i].text+"</p>");}
            if (context[i].images){
              $('#current').find('.date').before("<p>" + context[i].images +"</p>");
            }
            if(context[i].grey){
              console.log('unread');
              $('#current').css('background-color', 'rgb(247, 245, 245)');
            }
            else{
              console.log('read');
              $('#current').css('background-color', 'white');
            }
            $('#current').removeAttr("id");
            $('#current').attr('id', 'next');
        }
      },
      error: function(error) {
        alert('Error. Try again please!');
      }
   });
  }
});


$('#make-choice').one('click', function(e){
  e.preventDefault();
  red = $('.red-subscrib');
  var name =[];
  $('.red-subscrib').each(function(i, elem) {
    name.push($(elem).attr('name'));
  });
  console.log(name);
  $.ajax({
      type: 'POST',
      url: 'ajax_make_chat/',
      data: name,
      processData: false,
      success: function(context) {
        redir = "/messages/chat/" + context.chat_id + "/"
        $('.hidden-redirect').find('#redirect-form').attr("action", redir);
        $('.hidden-redirect').find('#redirect-form').submit();
              },
      error: function(error){
        alert('Error. Try again please!')
      }
  });
  return false;
});
