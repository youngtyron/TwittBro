$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
     number = $('.page-number').attr('name');
     $.ajax({
       data: number,
       type : 'GET',
       url : 'ajax_scroll_news/',
       processData: false,
       success : function(context){
         page = parseInt($('.page-number').attr('name')) + 1;
         $('.page-number').attr('name', page);
         for (i = 0; i < Object.keys(context).length; i++){
           if (context[i].you_liked){
             $('.post-column').append("<li class='list-group-item posts' ><div class = 'one-post' id = 'current' name = '" + context[i].id+ "'>" + " <a href='" + context[i].link  +
                                        "'><p>" + context[i].avatar + " " + context[i].f_n + " " + context[i].l_n + "</p></a><a href='"+context[i].post_link+"'><p class = 'post-date'>" +  context[i].date + "</p></a><i class='fas fa-heart' name = 'liking-from-news' id= '" +
                                        context[i].id + "' style ='color:red';>" + context[i].l_q + "</i><i class='fas fa-comment' name = '" + context[i].id + "'>" + context[i].c_q + "</i><p class ='show-comments' style ='color:rgb(0, 123, 255); display: none;'>Show all comments</p><ul class='list-group  com-column'></ul>" + "</div></li>");
                                      }
           else {
             $('.post-column').append("<li class='list-group-item posts'><div class = 'one-post' id = 'current' name = '" + context[i].id+ "'>" + " <a href='" + context[i].link  +
                                        "'><p>" + context[i].avatar + " " + context[i].f_n + " " + context[i].l_n + "</p></a><a href='"+context[i].post_link+"'><p class = 'post-date'>" +  context[i].date + "</p></a><i class='fas fa-heart' name = 'liking-from-news' id= '" +
                                        context[i].id + "'>" + context[i].l_q + "</i><i class='fas fa-comment' name = '" + context[i].id + "'>" + context[i].c_q + "</i><p class ='show-comments' style ='color:rgb(0, 123, 255); display: none;'>Show all comments</p><ul class='list-group  com-column'></ul>" + "</div></li>");
                                      }
            if (context[i].text){
              $('#current').find('.post-date').before("<p class = 'post-text'>"+context[i].text + "</p>");
            }
            if (context[i].images){
              $('#current').find('.post-date').parent().after("<p>" + context[i].images + "</p>");
            }
            if (context[i].comments){
              $('#current').find('.show-comments').css('display', 'block')
            }
            $('#current').find('.com-column').append(context[i].comments)
            token = $('[name="csrfmiddlewaretoken"]').val()
            $('#current').append("<form action='' method='post' class='comment-sent-from-news' name='empty'><div class='hidden-comment-form' style = 'display: none;'><input name='csrfmiddlewaretoken' value ='" + token
                                + "'type='hidden'><p><label for='id_comment-text'>Text:</label> <textarea name='comment-text' maxlength='500' cols='2' id='id_comment-text' rows='2' class='form-control'></textarea></p>" +
                                "<input value='Submit' class='btn btn-dark add-comment-news cust-button' type='submit'></div></form>");
            if (context[i].repost_button) {
              $('#current').find('.fa-heart').after(" "+"<i class='fas fa-external-link-square-alt' name = 'reposting-from-news'>"+context[i].r_q+"</i>"+" ")
            }
            else {
              $('#current').find('.fa-heart').after(" "+"<i class='fas fa-external-link-square-alt' name = 'my-post-repost'>"+context[i].r_q+"</i>"+" ")
            }
            if (context[i].delete_cross){
              $('#current').find('.post-text').parent().before("<i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;' name ='delete-from-news'></i>")
            }
            $('#current').removeAttr("id");

         }
       },
       error :  function(error){
         alert('Error. Try again please!')
       },
     });
   return false;
  }
});
