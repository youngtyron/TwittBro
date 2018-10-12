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

$(document).mouseup(function (e){
container = $(".gallery-container");
if (!container.is(e.target) && container.has(e.target).length === 0) {
    container.hide();
    $('#opened').removeAttr('id');
    $('#father-opened').removeAttr('id');
    }
});

$(document).on('click', '.add-member-link', (function(){
  $('.add-member-form').submit();
}));


$(document).on('mouseover', '.right-arrow', (function(){
  $(this).css('opacity', '1');
}));

$(document).on('mouseover', '.left-arrow', (function(){
  $(this).css('opacity', '1');
}));

$(document).on('mouseout', '.right-arrow', (function(){
  $(this).css('opacity', '0.1');
}));

$(document).on('mouseout', '.left-arrow', (function(){
  $(this).css('opacity', '0.1');
}));

$(document).on('click', '.avatar', (function(){
  if ($(this).attr('src') == "/static/images/default_ava.jpg"){
    alert("This user didn't add his avatar")
  }
  else{
    image = $(this).attr('name');
    $('.gallery-container').css('display','block');
    $('.gallery-window').html("<img src ='"+image+"'>");
  }
}));

$(document).on('click', '.right-arrow', (function(){
    next = $('#opened').next();
    if (next.parent().attr('id') == 'father-opened'){
      $('#opened').removeAttr('id');
      next.attr('id', 'opened');
      picture = next.attr('name');
      $('#image-on-gallery').attr('src', picture);
    }
    else {
      next = $('#father-opened').find('.mini-images').filter( ':first' );
      $('#opened').removeAttr('id');
      next.attr('id', 'opened');
      picture = next.attr('name');
      $('#image-on-gallery').attr('src', picture);
    }
}));

$(document).on('click', '.left-arrow', (function(){
    prev = $('#opened').prev();
    if (prev.parent().attr('id') == 'father-opened'){
      $('#opened').removeAttr('id');
      prev.attr('id', 'opened');
      picture = prev.attr('name');
      $('#image-on-gallery').attr('src', picture);
    }
    else {
      prev = $('#father-opened').find('.mini-images').filter( ':last' );
      $('#opened').removeAttr('id');
      prev.attr('id', 'opened');
      picture = prev.attr('name');
      $('#image-on-gallery').attr('src', picture);
    }
}));

$(document).on('click', '.mini-images', (function(){
  image = $(this).attr('name');
  $(this).attr('id', 'opened');
  $(this).parent().attr('id', 'father-opened');
  $('.gallery-container').css('display','block');
  if ($(this).parent().find('.mini-images').length >1){
    $('.gallery-window').html("<i class='far fa-arrow-alt-circle-left fa-3x left-arrow'></i>"+"<img id='image-on-gallery' src ='"+image+"'>"+"<i class='far fa-arrow-alt-circle-right fa-3x right-arrow'></i>");
  }
  else{
    $('.gallery-window').html("<img id='image-on-gallery' src ='"+image+"'>");
  }
}));

$('[name = "delete"]').mouseenter(function(){
  $(this).css('opacity', 1);
});

$('[name = "delete"]').mouseout(function(){
  $(this).css('opacity', 0.3);
});

$('[name = "delete-from-detail"]').mouseenter(function(){
  $(this).css('opacity', 1);
});

$('[name = "delete-from-detail"]').mouseout(function(){
  $(this).css('opacity', 0.3);
});

$('[name = "delete-from-news"]').mouseenter(function(){
  $(this).css('opacity', 1);
});

$('[name = "delete-from-news"]').mouseout(function(){
  $(this).css('opacity', 0.3);
});

$(document).on('mouseout', '[name = "delete-from-results"]', (function(){
  $(this).css('opacity', 1);
}));

$(document).on('mouseout', '[name = "delete-from-results"]', (function(){
  $(this).css('opacity', 0.3);
}));

$(document).on('click', '[name = "my-post-repost"]', (function(){
  alert("You can't cite your post");
}));

$(document).on('click', '.add-picture', function(){
  $('#id_image_message').click();
});

$(document).on('click', '.add-picture', function(){
  $('#id_image_post').click();
});

$(document).on('click', '.avatar-setting', (function(){
  $('.hidden-avatar-form').toggle();
}));

$(document).mouseup(function (e){ // событие клика по веб-документу
    if ($('.com-com-sent-from-detail').exists()){
      var el = $('.com-com-sent-from-detail'); // тут указываем  элемент
      var ex = $('.one-comment-detail');
      if (!el.is(e.target)// если клик был не по нашему блоку
          && !ex.is(e.target) && el.has(e.target).length === 0 && ex.has(e.target).length === 0) { // и не по его дочерним элементам
        el.attr('class', 'comment-sent-from-detail');
        $(".comment-sent-from-detail").attr('name', 'empty');
        $(".comment-sent-from-detail").removeAttr('id');
        $(".comment-sent-from-detail").find('.form-control').val('');
        }
    }
	});

$('#posting').keypress(function(e){
  if(e.keyCode==13){
    $(this).submit();
  }
});

$(document).on('click', '.one-comment-detail', (function(){
  name = $(this).find('.commentator-name').html().split(' ')[0];
  id = $(this).find('.commentator-name').attr('name');
  if ($('.comment-sent-from-detail').exists()){
    $('.comment-sent-from-detail').find('.form-control').val(name + ", ").focus();
    $('.comment-sent-from-detail').attr('name', id);
    id_com = $(this).attr('name');
    $('.comment-sent-from-detail').attr('id', id_com);
    $('.comment-sent-from-detail').attr('class', 'com-com-sent-from-detail');
  }
  else{
    id_com = $(this).attr('name');
    $('.com-com-sent-from-detail').attr('id', id_com);
    $('.com-com-sent-from-detail').find('.form-control').val(name + ", ").focus();
  }
}));

$('.searching').submit(function(){
  val = $('.form-control').val();
  if (val == ''){
    alert('Input something');
    return false;
  }
  else {
    return true;
  }
});

$(document).on('click', '.chat-settings', (function(){
  $('.hidden-chat-settings').toggle();
}));

$(document).on('click', '.show-chat-members', (function(){
  $('.chat-members').toggle();
}));

$(document).on('click', '#show-avatar-form', (function(){
  $('.hidden-avatar-form').toggle();
}));

$(document).on('click', '#show-changing-form', (function(){
  $('.hidden-name-form').toggle();
}));

$('.delete-confirm').click(function(){
  if(confirm('Your user profile will be permanently deleted')){
    return true;
  }
  else {
    return false;
  }
})

$('.email-flag').click(function(){
  $('.email-hidden-form').css('display', 'block');
  $('.email-flag').css('display', 'none');
});


$('#show-post-form').click(function(){
  $('.hidden-post-form').toggle();
});


$(document).ready(function() {
  red = $('#red-envelope');
  if (red.exists()){
    $('.fa-envelope').css('color', 'red');
  }
});

$('.one-subscrib').click(function(){
  $(this).css("border", "red solid 1px");
  $(this).attr('class', 'red-subscrib');

});

$('.go-to-chat').click(function(){
  $(this).find('.this_chat').submit();
});

$('#show-image-form').click(function(){
  $('#id_image').toggle();

});

$(document).ready(function() {
  notif = $('#notif').attr('name');
  if (notif == 'True') {
    $('.fa-bell').css('color', 'red');
  }
});

$(document).on('click','.fa-comment', (function(){
  com = $(this).parent();
  form = com.find('.hidden-comment-form').toggle();
}));

$.fn.extend({
    toggleText: function(a, b){
        return this.text(this.text() == b ? a : b);
    }
});


$(document).on('click', '.show-comments', (function(){
  $(this).toggleText('Hide all comments', 'Show all comments');
  comm = $(this).parent();
  comm.find('.com-column').toggle();
}));


$('.onme_subs').click(function(){
  $('.mysubs-group').css('display', 'none');
  $('.subs_onme_group').css('display', 'block');
});

$('.my_subs').click(function(){
  $('.mysubs-group').css('display', 'block');
  $('.subs_onme_group').css('display', 'none');
});

$('#to-write-message').click(function(){
  $('.hidden-message-form').toggle();
});
