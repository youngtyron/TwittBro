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


jQuery.fn.exists = function() {
   return $(this).length;
}

jQuery.fn.visible = function() {
  if((this).css('display')=='block'){
    return true;
  }
  else {
    return false;
  }
}


$(document).ready(function() {
  $('.access-confirm').click(function(e){
    e.preventDefault();
    if (confirm('Do you want to give this user access to your page?')){
      $.ajax({
        type: 'POST',
        url: 'ajax_give_access/',
        success: function(context){
          alert(context.f + ' ' + context.l + ' now has access to your page')
        },
        error : function(error){
          alert('Error. Try again please!')
        }
      });
      return false;
    }
  });
});


$(document).ready(function() {
  $('.black-book').click(function(e){
    e.preventDefault();
    if (confirm('Do you want to forbid an access to your page for this user?')){
      $.ajax({
        type: 'POST',
        url: 'ajax_black_book/',
        success: function(context){
          alert(context.f + " " + context.l + " now hasn't access to your page")
        },
        error : function(error){
          alert('Error. Try again please!')
        }
      });
      return false;
    }
  });
});



$(document).ready(function() {
    $('#messaging').ajaxForm({
      type : 'POST',
      dataType: "json",
      url : 'ajax_write/',
      clearForm : true,
      success: function (context) {
        if (context.too_much){
          alert('You can send no more than 10 images')
        }
        else if (context.sent){
          alert('Message is sent');
          $('.hidden-message-form').css('display', 'none');
        }
      },
      error: function (error) {
        alert('Error. Try again please!');
      }
    });
});




$(document).ready(function() {
    $('#posting').ajaxForm({
      type : 'POST',
      dataType: "json",
      url : 'ajax_post/',
      clearForm : true,
      success: function (context) {
        if (context.too_much){
          alert('You can send no more than 10 images')
        }
        else if (context.images == null && context.text != null){
          $('#post-list').prepend("<li class = 'list-group-item'> <p>" + context.text + "</p> <p> Right now </p><i class='fas fa-heart liked' name = 'liking' id= '" +context.id + "'>0</i></li>");
        }
        else if (context.images != null && context.text != null) {
          $('#post-list').prepend("<li class = 'list-group-item'> <p>" + context.text + "</p><p>" + context.images + "</p><p> Right now </p></li>");
        }
        else if (context.text == null && context.images != null){
          $('#post-list').prepend("<li class = 'list-group-item''> <p>" + context.images + "</p><p> Right now </p></li>");
        }
      },
      error: function (error) {
        alert('Error. Try again please!');
      }
    });
});


$('.change-status').click(function(e){
    e.preventDefault();
    $('.status-enter').css('display', 'block');
});

$('.form-status').submit(function(e){
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: 'ajax_status/',
      data: $('.status-enter').serialize(),
      processData: false,
      success: function(context){
        $('.status-enter').css('display', 'none');
        $('.str-status').css('display', 'none');
        $('.status').prepend("<p class ='str-status'>"+ context.status + "</p>");
      },
      error : function(error){
        alert('Error. Try again please!')
      }

    });
  return false;
});


$('.form-status-from-news').submit(function(e){
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: 'ajax_status_from_news/',
      data: $('.status-enter').serialize(),
      processData: false,
      success: function(context){
        $('.status-enter').css('display', 'none');
        $('.str-status').css('display', 'none');
        $('.status').prepend("<p class ='str-status'>"+ context.status + "</p>");
      },
      error : function(error){
        alert('Error. Try again please!')
      }

    });
  return false;
});



$(document).on('click', '[name = "liking"]', (function(e){
  e.preventDefault();
  post_id = $(this).attr('id');
  color = $(this).css('color');
  $(this).attr('id', 'in-work');
  $.ajax({
    type : 'POST',
    url : 'ajax_like/',
    data: post_id,
    processData: false,
    success : function(context){
      num = $('#in-work');
      num.html(context.num_likes);
      num.attr('id', context.post_id);
      if (color == 'rgb(255, 0, 0)'){
        num.css('color', "black");
      }
      else {
        num.css('color', "red");
      }
    } ,
    error :  function(error){
      alert('Error. Try again please!')
    },
  });
return false;
}));


$(document).on('click', '[name = "liking-from-news"]',(function(e){
  e.preventDefault();
  post_id = $(this).attr('id');
  color = $(this).css('color');
  $(this).attr('id', 'in-work');
  $.ajax({
    type : 'POST',
    url : 'ajax_like_from_news/',
    data: post_id,
    processData: false,
    success : function(context){
      num = $('#in-work');
      num.html(context.num_likes);
      num.attr('id', context.post_id);
      if (color == 'rgb(255, 0, 0)'){
        num.css('color', "black");
      }
      else {
        num.css('color', "red");
      }
    } ,
    error :  function(error){
      alert('Error. Try again please!')
    },
  });
return false;
}));


$(document).on('click','[name = "delete"]', (function(e){
  if(confirm('Do you want to delete this post?')){
    e.preventDefault();
    par = $(this).parent();
    post_id = $(par).attr('name');
    $(par).attr('name', 'in-work');
    $.ajax({
      type: 'POST',
      url: 'ajax_post_delete/',
      data: post_id,
      processData: false,
      success: function(){
        li = $('[name ="in-work"]').parent();
        li.remove();

      },
      error:function(){
        alert('Error. Try again please!')
      },
    });
    return false;
  };
}));


$(document).on('click','[name = "delete-from-news"]', (function(e){
  if(confirm('Do you want to delete this post?')){
    e.preventDefault();
    par = $(this).parent();
    post_id = $(par).attr('name');
    console.log(par);
    $(par).attr('name', 'in-work');
    $.ajax({
      type: 'POST',
      url: 'ajax_post_delete_from_news/',
      data: post_id,
      processData: false,
      success: function(){
        li = $('[name ="in-work"]').parent();
        li.remove();

      },
      error:function(){
        alert('Error. Try again please!')
      },
    });
    return false;
  };
}));



$(document).on('click','[name = "reposting"]', (function(e){
  if(confirm('Repost this on your page?')){
    e.preventDefault();
    par = $(this).parent();
    post_id = $(par).attr('name');
    $(par).attr('name', 'in-work');
    $.ajax({
      type : 'POST',
      url : 'ajax_repost/',
      data: post_id,
      processData: false,
      success : function(context){
          dad = $('[name ="in-work"]');
          num = dad.children('[name = "reposting"]');
          num.html(context.num_reposts);
          dad.attr('name', context.post_id);
        } ,
    error :  function(error){
      alert('Error. Try again please!')
    }
    });
    return false;
  };
}));

$(document).on('click','[name = "reposting-from-news"]', (function(e){
  if(confirm('Repost this on your page?')){
    e.preventDefault();
    par = $(this).parent();
    post_id = $(par).attr('name');
    $(par).attr('name', 'in-work');
    $.ajax({
      type : 'POST',
      url : 'ajax_repost_from_news/',
      data: post_id,
      processData: false,
      success : function(context){
          dad = $('[name ="in-work"]');
          num = dad.children('[name = "reposting"]');
          num.html(context.num_reposts);
          dad.attr('name', context.post_id);
        } ,
    error :  function(error){
      alert('Error. Try again please!')
    }
    });
    return false;
  };
}));



$('.subs-button').click(function(e){
  e.preventDefault();
  chil = $(this).children('[type = "button"]');
  but = chil.attr('id');
  if (but == 'subscribe'){
    alert('Do you want to subscribe?');
    $.ajax({
          type: 'POST',
          url: 'ajax_simple_subscribe/',
          processData: false,
          success: function(context){
                          $('#subscribe').attr('class', 'btn btn-outline-info');
                          $('#subscribe').html('Unsubscribe');
                          $('#subscribe').attr('id', 'unsubscribe');
                          alert('You subscribed to ' + context.first_name + ' ' + context.last_name);
                    },
        });
        return false;
  }
  else if (but == 'unsubscribe'){
    alert('Do you want to cancel a subscription?')
    $.ajax({
          type: 'POST',
          url: 'ajax_simple_unsubscribe/',
          processData: false,
          success: function(context){
                          $('#unsubscribe').attr('class', 'btn btn-info');
                          $('#unsubscribe').html('Subscribe');
                          $('#unsubscribe').attr('id', 'subscribe')
                          alert('You canceled  a subscription to ' + context.first_name + ' ' + context.last_name)
                    },
        });
        return false;
  }

});


$(document).on('click', '.one-comment', (function(){
  par = $(this).parent();
  id2 = $(this).attr('name');
  $('.com-com-sent').css('display:block');
  if ($('.hidden-com-com-form').visible()){
    form = par.siblings().find('.hidden-com-com-form').css('display:none');
  }
  else{
    form = par.siblings().find('.hidden-com-com-form').css('display:block');
  }
  $('.com-com-sent').ajaxForm({
    type: 'POST',
    dataType: 'json',
    data: {id2: id2 },
    clearForm: true,
    url: 'ajax_comment_comment/',
    success: function(context){
      col = $('.com-column').find('[name = ' + context.com_id + ']').parent();
      col.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p> <a href='http://localhost:8000/" + context.man_id +  "'>" + context.who + '</a>, ' + context.text + "</p> <p>Right now</p></li>");
    },
    error: function(error) {
      alert('Error. Try again please!')
    }
  });
}));



 $(document).on('click', '.add-comment', (function(){
   par = $(this).parents('.one-post');
   id = par.attr('name');
   $('.comment-sent').ajaxForm({
     type: 'POST',
     dataType: 'json',
     data: {id: id },
     clearForm: true,
     url: 'ajax_comment/',
     success: function(context){
       list = $('.posts').find('[name = ' + context.id + ']').find('.com-column').show();
       list.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p>" + context.text + "</p> <p>Right now</p></li>");

     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));

 $(document).on('click', '.add-comment', (function(){
   par = $(this).parents('.one-post');
   id = par.attr('name');
   $('.comment-sent-from-news').ajaxForm({
     type: 'POST',
     dataType: 'json',
     data: {id: id },
     clearForm: true,
     url: 'ajax_comment_from_news/',
     success: function(context){
       list = $('.posts').find('[name = ' + context.id + ']').find('.com-column').show();
       list.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p>" + context.text + "</p> <p>Right now</p></li>");
     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));

 $(document).on('click', '.one-comment', (function(){
   par = $(this).parent();
   id2 = $(this).attr('name');
   $('.com-com-sent-from-news').css('display:block');
   form = par.siblings().find('.hidden-com-com-form').toggle();
   $('.com-com-sent-from-new').ajaxForm({
     type: 'POST',
     dataType: 'json',
     data: {id2: id2 },
     clearForm: true,
     url: 'ajax_comment_comment_from_news/',
     success: function(context){
       col = $('.com-column').find('[name = ' + context.com_id + ']').parent();
       col.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p> <a href='http://localhost:8000/" + context.man_id +  "'>" + context.who + '</a>, ' + context.text + "</p> <p>Right now</p></li>");
     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));
