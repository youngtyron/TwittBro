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

$(document).on('click', '.avatar-deleting', (function() {
  if (confirm("Are you sure want to delete your avatar image?")){
    $.ajax({
      type: 'POST',
      url: 'ajax_avatar_remove/',
      success: function(context){
        $('.avatar').attr('src', '/static/images/default_ava.jpg');
        $('.avatar').attr('name', '/static/images/default_ava.jpg');
      },
      error : function(error){
        alert('Error. Try again please!')
      }
    });
    return false;
  }
}));

$(document).ready(function() {
    $('.avatarizing-form').ajaxForm({
      type : 'POST',
      dataType: "json",
      url : 'ajax_avatarize/',
      clearForm : true,
      success: function (context) {
        console.log(context)
        $('#step-switch').html("Next step");
        $('#avatar-exhibit').attr('src', context.avatar);
      },
      error: function (error) {
        alert('Error. Try again please!');
      }
    });
});

$(document).on('click', '.save-changes', (function() {
    $('.edit-profile-form').ajaxForm({
      type : 'POST',
      dataType: "json",
      url : 'ajax_update_profile/',
      clearForm : true,
      success: function (context) {
        if (context.email){
          $('.email-hidden-form').css('display', 'none');
          $('.email-flag').css('display', 'block');
          $('.email-flag').html("Email: "+context.email)
        }
        if (context.closed){
          $('.open-or-close').html("Open your profile for all users? <input type='checkbox' name='private' value='open-it' style = 'margin-top: 10px;'>")
        }
        if (context.opened){
          $('.open-or-close').html("Make your profile private? <input type='checkbox' name='private' value='close-it' style = 'margin-top: 10px;'> ")
        }
        if (context.avatar){
          $('.avatar').replaceWith(context.avatar);
        }
        alert('Profile is updated')
      },
      error: function (error) {
        alert('Error. Try again please!');
      }
    });
}));


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
        if (context.empty){
          alert('Input something')
        }
        else if (context.too_much){
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
            if (context.empty){
              alert('Input something')
            }
            if (context.too_much){
              alert('You can send no more than 10 images')
            }
            else if (context.images == null && context.text != null){
              $('#post-list').prepend("<li class = 'list-group-item posts' id = 'current'><div class = 'one-post' name = '"+context.id+"'> <i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;'' name ='delete'></i><p>" + context.text + "</p> <p> Right now </p></div></li>");
            }
            else if (context.images != null && context.text != null) {
              $('#post-list').prepend("<li class = 'list-group-item posts' id = 'current'><div class = 'one-post' name = '"+context.id+"'> <i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;'' name ='delete'></i><p>" + context.text + "</p><p>" + context.images + "</p><p> Right now </p></div></li>");
            }
            else if (context.text == null && context.images != null){
              $('#post-list').prepend("<li class = 'list-group-item posts' id = 'current'><div class = 'one-post' name = '"+context.id+"'> <i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;'' name ='delete'></i><p>" + context.images + "</p><p> Right now </p></div></li>");
            }
            $('#current').find('.one-post').append("<i class='fas fa-heart not-liked' name = 'liking' id= '" +context.id + "'>0</i>");
            $('#current').find('.one-post').append("<i class='fas fa-comment' name = '"+context.id +"'>0</i>");
            token = $('[name="csrfmiddlewaretoken"]').val();
            $('#current').find('.one-post').append("<ul class='list-group  com-column'></ul>");
            $('#current').find('.one-post').append("<form action='' method='post' class= 'comment-sent' name = 'empty'><div class='hidden-comment-form'  style = 'display: none;'>" +
                                                    "<input name='csrfmiddlewaretoken' value='"+token+"' type='hidden'>" +
                                                    "<p><label for='id_comment-text'>Text:</label> <textarea name='comment-text' cols='2' maxlength='500' class='form-control' rows='2' id='id_comment-text'></textarea></p><input type='submit' value = 'submit' class ='btn btn-dark cust-button add-comment'></div></form>");
            $('#current').find('.one-post').append("<form action='' method='post' class='com-com-sent' name='empty'><div class='hidden-com-com-form' style= 'display: none;'><input name='csrfmiddlewaretoken' value='"+
                                                    token +"' type='hidden'><p><label for='id_com_com-text'>Text:</label> <textarea name='com_com-text' rows='2' cols='2' maxlength='500' class='form-control' id='id_com_com-text'></textarea></p><input value='submit' class='btn btn-dark add-com-com cust-button' type='submit'></div></form>")
            $('#current').removeAttr("id");
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


$(document).on('click', '[name ="liking-from-detail"]', function(e){
  e.preventDefault();
  color = $(this).css('color');
  $.ajax({
    type : 'POST',
    url : 'ajax_like/',
    processData: false,
    success : function(context){
      $('[name ="liking-from-detail"]').html(context.num_likes);
      if (color == 'rgb(255, 0, 0)'){
        $('[name ="liking-from-detail"]').css('color', "black");
      }
      else{
        $('[name ="liking-from-detail"]').css('color', "red");
      }
    } ,
    error :  function(error){
      alert('Error. Try again please!')
    },
  });
return false;
});

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

$(document).on('click', '[name = "liking-from-results"]',(function(e){
  e.preventDefault();
  post_id = $(this).attr('id');
  color = $(this).css('color');
  $(this).attr('id', 'in-work');
  $.ajax({
    type : 'POST',
    url : 'ajax_like_from_results/',
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

$(document).on('click','[name = "delete-from-results"]', (function(e){
  if(confirm('Do you want to delete this post?')){
    e.preventDefault();
    par = $(this).parent();
    post_id = $(par).attr('name');
    $(par).attr('name', 'in-work');
    $.ajax({
      type: 'POST',
      url: 'ajax_post_delete_from_results/',
      data: post_id,
      processData: false,
      success: function(){
        li = $('[name ="in-work"]');
        li.remove();

      },
      error:function(){
        alert('Error. Try again please!')
      },
    });
    return false;
  };
}));


$(document).on('click','[name = "delete-from-detail"]', (function(e){
  if(confirm('Do you want to delete this post?')){
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: 'ajax_post_delete_from_detail/',
      processData: false,
      success: function(){
        $('.post-square').html("<p style='text-center'>This post is deleted</p>");
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
          if(context.already_reposted){
            alert("You can't repost it twice")
          }
          else{
            if (context.num_reposts){
              dad = $('[name ="in-work"]');
              num = dad.children('[name = "reposting"]');
              num.html(context.num_reposts);
              dad.attr('name', context.post_id);
              alert('This post was cited!')
            }
            else {
              $('[name ="in-work"]').attr('name', context.post_id);
              alert('This post was cited!')
            }
          }
        } ,
    error :  function(error){
      alert('Error. Try again please!')
    }
    });
    return false;
  };
}));

$(document).on('click','[name = "reposting-from-detail"]', (function(e){
  if(confirm('Repost this on your page?')){
    e.preventDefault();
    $.ajax({
      type : 'POST',
      url : 'ajax_repost/',
      processData: false,
      success : function(context){
          if(context.already_reposted){
            alert("You can't repost it twice")
          }
          else{
              $('[name = "reposting-from-detail"]').html(context.num_reposts);
              alert('This post was cited!');
            }
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
    $(this).attr('name', 'in-work');
    $.ajax({
      type : 'POST',
      url : 'ajax_repost_from_news/',
      data: post_id,
      processData: false,
      success : function(context){
        if(context.already_reposted){
          alert("You can't repost it twice")
        }
        else {
          $('[name ="in-work"]').html(context.num_reposts).attr('name', 'reposting-from-news');
          alert('This post was cited!')
        }
        } ,
    error :  function(error){
      alert('Error. Try again please!')
    }
    });
    return false;
  };
}));

$(document).on('click','[name = "reposting-from-results"]', (function(e){
  if(confirm('Repost this on your page?')){
    e.preventDefault();
    par = $(this).parent();
    post_id = $(par).attr('name');
    $(this).attr('name', 'in-work');
    $.ajax({
      type : 'POST',
      url : 'ajax_repost_from_results/',
      data: post_id,
      processData: false,
      success : function(context){
        if(context.already_reposted){
          alert("You can't repost it twice")
        }
        else {
          $('[name ="in-work"]').html(context.num_reposts).attr('name', 'reposting-from-results');
          alert('This post was cited!')
        }
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
  x = $(this).parent().siblings().find('.hidden-comment-form').css('display', 'block');
  x.parent().attr('class', 'com-com-sent');
  name = $(this).find('.commentator-name').html().split(' ')[0];
  $('.com-com-sent').find('.form-control').val(name + ', ');
      $('.com-com-sent').ajaxForm({
        type: 'POST',
        dataType: 'json',
        data: {id2: id2 },
        clearForm: true,
        url: 'ajax_comment_comment/',
        success: function(context){
          if (context.empty){
            alert('Input something')
          }
          else {
            col = $('.com-column').find('[name = ' + context.com_id + ']').parent();
            col.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p> <a href='http://localhost:8000/" + context.man_id +  "'>" + context.who + '</a>, ' + context.text + "</p> <p>Right now</p></li>");
            $('.com-com-sent').children().hide();
            $('.com-com-sent').attr('class', 'comment-sent');
          }
        },
        error: function(error) {
          alert('Error. Try again please!');
          $('.com-com-sent').children().hide();
          $('.com-com-sent').attr('class', 'comment-sent');
        }
      });
}));

function Remove(str, startIndex) {
    return str.substr(0, startIndex);
}

$(document).on('click', '.one-comment-news', (function(){
  par = $(this).parent();
  id2 = $(this).attr('name');
  x = $(this).parent().siblings().find('.hidden-comment-form').css('display', 'block');
  x.parent().attr('class', 'com-com-sent-from-news');
  name = $(this).find('.commentator-name').html().split(' ')[0];
  $('.com-com-sent-from-news').find('.form-control').val(name + ', ');
      $('.com-com-sent-from-news').ajaxForm({
        type: 'POST',
        dataType: 'json',
        data: {id2: id2 },
        clearForm: true,
        url: 'ajax_comment_comment/',
        success: function(context){
          if (context.empty){
            alert('Input something')
          }
          else {
            col = $('.com-column').find('[name = ' + context.com_id + ']').parent();
            col.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p> <a href='http://localhost:8000/" + context.man_id +  "'>" + context.who + '</a>, ' + context.text + "</p> <p>Right now</p></li>");
          }
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
       if (context.empty){
         alert('Input something')
       }
       else {
         list = $('.posts').find('[name = ' + context.id + ']').find('.com-column').append("<li class='list-group-item one-comment' name ='"+context.com_id+"'> <p>" + context.f_n + " " + context.l_n + "</p> <p>" + context.text + "</p> <p>Right now</p></li>");;
         list.show();
       }
     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));

 $(document).on('click', '.add-comment-news', (function(){
   par = $(this).parents('.one-post');
   id = par.attr('name');
   $('.comment-sent-from-news').ajaxForm({
     type: 'POST',
     dataType: 'json',
     data: {id: id },
     clearForm: true,
     url: 'ajax_comment/',
     success: function(context){
       if (context.empty){
         alert('Input something')
       }
       else {
         list = $('.posts').find('[name = ' + context.id + ']').find('.com-column').show();
         list.append("<li class='list-group-item'> <p class ='commentator-name'>" + context.f_n + " " + context.l_n + "</p> <p>" + context.text + "</p> <p>Right now</p></li>");
       }
     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));

 $(document).on('click', '.add-comment-results', (function(){
   par = $(this).parents('.posts');
   id =  par.attr('name');
   $('.comment-sent-from-results').ajaxForm({
     type: 'POST',
     dataType: 'json',
     data: {id: id },
     clearForm: true,
     url: 'ajax_comment/',
     success: function(context){
       if (context.empty){
         alert('Input something')
       }
       else {
         list = $('.posts').closest('[name = ' + context.id + ']').find('.com-column').show();
         list.append("<li class='list-group-item'> <p>" + context.f_n + " " + context.l_n + "</p> <p>" + context.text + "</p> <p>Right now</p></li>");
       }
     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));

 $(document).on('click', '.one-comment-results', (function(){
   par = $(this).parent();
   id2 = $(this).attr('name');
   x = $(this).parent().siblings().find('.hidden-comment-form').css('display', 'block');
   x.parent().attr('class', 'com-com-sent-from-results');
   name = $(this).find('.commentator-name').html().split(' ')[0];
   $('.com-com-sent-from-results').find('.form-control').val(name + ', ');
   $('.com-com-sent-from-results').ajaxForm({
     type: 'POST',
     dataType: 'json',
     data: {id2: id2 },
     clearForm: true,
     url: 'ajax_comment_comment/',
     success: function(context){
       if (context.empty){
         alert('Input something')
       }
       else {
         col = $('.com-column').find('[name = ' + context.com_id + ']').parent();
         col.append("<li class='list-group-item'> <p class ='commentator-name'>" + context.f_n + " " + context.l_n + "</p> <p> <a href='http://localhost:8000/" + context.man_id +  "'>" + context.who + '</a>, ' + context.text + "</p> <p>Right now</p></li>");
       }
     },
     error: function(error) {
       alert('Error. Try again please!')
     }
   });
 }));

 $(document).on('click', '.add-comment-detail', (function(){
   if ($('.comment-sent-from-detail').exists()){
     $('.comment-sent-from-detail').ajaxForm({
       type: 'POST',
       dataType: 'json',
       clearForm: true,
       url: 'ajax_comment/',
       success: function(context){
         if (context.empty){
           alert('Input something')
         }
         else {
           if ($('#no-comments').exists()){
             $('#no-comments').remove();
           }
           $('.comments').append("<li class='list-group-item' name ='"+context.com_id+"'> <p class = 'commentator-name' name ='"+context.my_id+"'>" + context.f_n + " " + context.l_n + "</p> <p>" + context.text + "</p> <p>Right now</p></li>");
           $('.comments-title').html(context.num + " Comments");
         }
       },
       error: function(error) {
         alert('Error. Try again please!')
       }
     });
     }
  else if ($('.com-com-sent-from-detail').exists()){
    id_to = $('.com-com-sent-from-detail').attr('name');
    id_com = $('.com-com-sent-from-detail').attr('id');
    $('.com-com-sent-from-detail').removeAttr('id');
    $('.com-com-sent-from-detail').attr('name', 'empty');
    $('.com-com-sent-from-detail').ajaxForm({
      type: 'POST',
      dataType: 'json',
      data: {id_to: id_to,
             id_com: id_com},
      clearForm: true,
      url: 'ajax_comment_comment/',
      success: function(context){
        if (context.empty){
          alert('Input something')
        }
        else{
          $('.comments').append("<li class='list-group-item' name ='"+context.com_id+"'> <p class = 'commentator-name' name ='"+context.my_id+"'>" + context.f_n + " " + context.l_n + "</p> <p> <a href='http://localhost:8000/" +
                                  context.man_id +  "'>" + context.who + '</a>, ' + context.text + "</p> <p>Right now</p></li>");
          $('.comments-title').html(context.num + " Comments");
        }
      },
      error: function(error) {
        alert('Error. Try again please!')
      }
    });
  }

 }));
