$('[name = "delete"]').mouseenter(function(){
  $(this).css('opacity', 1);
});

$('[name = "delete"]').mouseout(function(){
  $(this).css('opacity', 0.3);
});


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


$('.save-changes').click(function(){
  $('.edit-profile-form').submit();
  $('.edit-profile-form').reset();
});

// setInterval(function(){
//     location.reload();
// }, 5*60*1000);

$('#show-post-form').click(function(){
  $('.hidden-post-form').toggle();
});

$(document).ready(function() {
  sign = $('#sign').attr('name');
  if (sign == 'True') {
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
