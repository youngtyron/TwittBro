$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
     number = $('.page-number').attr('name');
     $.ajax({
       data: number,
       type : 'POST',
       url : 'ajax_scroll_wall/',
       processData: false,
       success : function(context){
         page = parseInt($('.page-number').attr('name')) + 1;
         $('.page-number').attr('name', page);
         for (i = 0; i < Object.keys(context).length; i++){
           $('#post-list').append("<li class='list-group-item posts'><div class = 'one-post' id = 'current' name = '"+context[i].id+"'><p class = 'post-date'>"+context[i].pub_date+"</p></div></li>");
           if(context[i].text){
             $('#current').find('.post-date').before("<p class = 'post-text'>"+context[i].text+"</p>");
           }
           if(context[i].images){
             $('#current').find('.post-date').after("<p>"+context[i].images+"</p>")
           }
           if(context[i].repost){
             $('#current').find('.post-text').before("<a href = '"+context[i].author_link+"'><p>"+context[i].f_n+" "+context[i].l_n+"</p></a>")
           }
           if (context[i].red){
             $('#current').find('.post-date').after("<i class='fas fa-heart liked' name = 'liking' id= '"+context[i].id+"'  style ='color:red';>"+context[i].l_q+"</i>");
           }
           else{
             $('#current').find('.post-date').after("<i class='fas fa-heart not-liked' name = 'liking' id= '"+context[i].id+"'  style ='color:black';>"+context[i].l_q+"</i>");
           }
           $('#current').find('.fa-heart').after("<i class='fas fa-comment' name = '"+context[i].id+"'>"+context[i].c_q+"</i><p class ='show-comments' style ='color:rgb(0, 123, 255); display: none;'>Show all comments</p><ul class='list-group  com-column'></ul>")

           if(context[i].your_post){
             $('#current').find('.post-text').before("<i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;' name ='delete'></i>");
           }
           else{
             $('#current').find('.fa-heart').after("<i class='fas fa-external-link-square-alt' name = 'reposting'>"+context[i].r_q+"</i>");
           }
           if (context[i].comments){
             $('#current').find('.show-comments').css('display', 'block')
             $('#current').find('.com-column').append(context[i].comments)
           }
           token = $('[name="csrfmiddlewaretoken"]').val()
           $('#current').append("<form action='' method='post' class='comment-sent' name='empty'><div class='hidden-comment-form' style = 'display: none;'><input name='csrfmiddlewaretoken' value ='" + token
                               + "'type='hidden'><p><label for='id_comment-text'>Text:</label> <textarea name='comment-text' maxlength='500' cols='2' id='id_comment-text' rows='2' class='form-control'></textarea></p>" +
                               "<input value='submit' class='btn btn-dark add-comment' type='submit'></div></form>" + "<form action='' method='post' class='com-com-sent' name='empty'><div class='hidden-com-com-form' style = 'display: none;'><input name='csrfmiddlewaretoken' value ='" + token
                               + "'type='hidden'><p><label for='id_com_com-text'>Text:</label> <textarea name='com_com-text' class='form-control' id='id_com_com-text' maxlength='500' cols='2' rows='2'></textarea></p>" +
                               "<input value='submit' class='btn btn-dark add-com-com' type='submit'></div></form>");
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
