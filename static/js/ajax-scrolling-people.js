$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
     number = $('.page-number').attr('name');
     $.ajax({
       data: number,
       type : 'GET',
       url : 'ajax_scroll_people/',
       processData: false,
       success : function(context){
         page = parseInt($('.page-number').attr('name')) + 1;
         $('.page-number').attr('name', page);
         for (i = 0; i < Object.keys(context).length; i++){
           if (context[i].you){
             $('.people-column').append("<a href="+context[i].link+" style='color: black; text-decoration: none;'><li class='list-group-item'  style='width:700px!important; margin-left: auto; margin-right: auto;'><p class='people_elem'>" +
                                       context[i].ava+  context[i].f_n+" "+context[i].l_n+" " + "  <span class='badge badge-primary'>You</span>"+ " "+context[i].followers+" followers</p</li></a>");
           }
           else if (context[i].you_follow){
             $('.people-column').append("<a href="+context[i].link+" style='color: black; text-decoration: none;'><li class='list-group-item' style='width:700px!important; margin-left: auto; margin-right: auto;'><p class='people_elem'>" +
                                        context[i].ava+  context[i].f_n+" "+context[i].l_n+" " + "  <span class='badge badge-success'>You follow</span>"+ " "+context[i].followers+" followers</p</li></a>");
           }
           else if (context[i].follow_you){
             $('.people-column').append("<a href="+context[i].link+" style='color: black; text-decoration: none;'><li class='list-group-item' style='width:700px!important; margin-left: auto; margin-right: auto;'><p class='people_elem'>" +
                                        context[i].ava+ context[i].f_n+" "+context[i].l_n+" " + "  <span class='badge badge-danger'>Follow you</span>"+ " "+context[i].followers+" followers</p</li></a>");
           }
           else{
             $('.people-column').append("<a href="+context[i].link+" style='color: black; text-decoration: none;'><li class='list-group-item' style='width:700px!important; margin-left: auto; margin-right: auto;'><p class='people_elem'>" +
                                        context[i].ava+ context[i].f_n+" "+context[i].l_n+ " "+context[i].followers+" followers</p</li></a>");
           }
         }
       },
       error :  function(error){
         alert('Error. Try again please!')
       },
     });
   return false;
  }
});
