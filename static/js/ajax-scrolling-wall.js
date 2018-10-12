$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
     number = $('.page-number').attr('name');
     $.ajax({
       data: number,
       type : 'GET',
       url : 'ajax_scroll_wall/',
       processData: false,
       success : function(context){
         page = parseInt($('.page-number').attr('name')) + 1;
         $('.page-number').attr('name', page);
         for (i = 0; i < Object.keys(context).length; i++){
           if(context[i].text){
             $('#post-list').append("<li class='list-group-item posts'><div class = 'one-post' id = 'current' name = '"+context[i].id+"'><a class='postlink' href = '"+context[i].post_link+"'><p class = 'post-text'>"+context[i].text+"</p><p class = 'post-date'>"+context[i].pub_date+"</p></a></div></li>");
           }
           else{
             $('#post-list').append("<li class='list-group-item posts'><div class = 'one-post' id = 'current' name = '"+context[i].id+"'><a class='postlink' href = '"+context[i].post_link+"'><p class = 'post-date'>"+context[i].pub_date+"</p></a></div></li>");
           }
           if(context[i].images){
             $('#current').find('.postlink').after("<p>"+context[i].images+"</p>")
           }
           if(context[i].repost){
             $('#current').find('.postlink').before("<a href = '"+context[i].author_link+"'><p>"+context[i].f_n+" "+context[i].l_n+"</p></a>")
           }
           if (context[i].red){
             $('#current').find('.postlink').after("<i class='fas fa-heart liked' name = 'liking' id= '"+context[i].id+"'  style ='color:red';>"+context[i].l_q+"</i>");
           }
           else{
             $('#current').find('.postlink').after("<i class='fas fa-heart not-liked' name = 'liking' id= '"+context[i].id+"'  style ='color:black';>"+context[i].l_q+"</i>");
           }
           $('#current').find('.fa-heart').after("<i class='fas fa-comment' name = '"+context[i].id+"'>"+context[i].c_q+"</i><p class ='show-comments' style ='color:rgb(0, 123, 255); display: none;'>Show all comments</p><ul class='list-group  com-column'></ul>")

           if(context[i].your_post){
             $('#current').find('.postlink').before("<i class='fas fa-times' style ='position: absolute; right: 5%; left: 95%;' name ='delete'></i>");
             $('#current').find('.fa-heart').after("<i class='fas fa-external-link-square-alt' name = 'my-post-repost'>"+context[i].r_q+"</i>");
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
                               "<input value='Submit' class='btn btn-dark add-comment cust-button' type='submit'></div></form>");
           $('#current').removeAttr("id");
         }
       },

     });
   return false;
  }
});
