$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
     number = $('.page-number').attr('name');
     $.ajax({
       data: number,
       type : 'GET',
       url : 'ajax_scroll_postresults/',
       processData: false,
       success : function(context){
         page = parseInt($('.page-number').attr('name')) + 1;
         $('.page-number').attr('name', page);
         for (i = 0; i < Object.keys(context).length; i++){
           $('.result-column').append("<li class='list-group-item posts' name ='"+context[i].id+"' id = 'current'><a href = '"+context[i].link+"'><p>"+context[i].avatar+" "+context[i].f_n+" "+context[i].l_n+"</p></a><a href = '"+context[i].post_link+"'><p class = 'post-text'>"+context[i].text+"</p><p class = 'post-date'>"+context[i].pub_date+"</p></a></li>")
           if (context[i].red){
             $('#current').append("<i class='fas fa-heart' name = 'liking-from-results' id= '"+context[i].id+"' style ='color:red';>"+context[i].l_q+"</i>");
           }
           else {
             $('#current').append("<i class='fas fa-heart' name = 'liking-from-results' id= '"+context[i].id+"'>"+context[i].l_q+"</i>");
           }
           if (context[i].can_repost){
             $('#current').append("<i class='fas fa-external-link-square-alt' name = 'reposting-from-results'>"+context[i].r_q+"</i>");
           }
           else{
             $('#current').append("<i class='fas fa-external-link-square-alt' name = 'my-post-repost'>"+context[i].r_q+"</i>");
           }
           $('#current').append("<i class='fas fa-comment'>"+context[i].c_q+"</i>");
           $('#current').append("<p class ='show-comments' style ='color:rgb(0, 123, 255); display: none;'>Show all comments</p><ul class='list-group com-column'></ul>");
           if (context[i].comments){
             $('#current').find('.show-comments').css('display', 'block');
             $('#current').find('.com-column').append(context[i].comments);
           }
           token = $('[name="csrfmiddlewaretoken"]').val()
           $('#current').append("<form action='' method='post' class='comment-sent-from-results' name='empty'><div class='hidden-comment-form' style = 'display: none;'><input name='csrfmiddlewaretoken' value ='" + token
                               + "'type='hidden'><p><label for='id_comment-text'>Text:</label> <textarea name='comment-text' maxlength='500' cols='2' id='id_comment-text' rows='2' class='form-control'></textarea></p>" +
                               "<input value='Submit' class='btn btn-dark add-comment-results cust-button' type='submit'></div></form>");
          if (context[i].delete_cross){
            $('#current').find('.post-text').parent().before("<i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;' name ='delete-from-results'></i>")
          }
          if (context[i].images){
            $('#current').find('.post-date').parent().after("<p>"+context[i].images+"</p>");
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
