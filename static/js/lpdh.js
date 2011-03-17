$(function(){
    $(".sideBoxHeader img").toggle(function(){
                                $(this).parent('.sideBoxHeader').next().slideUp();
                                var img = $(this);
                                img.attr('src', img.attr('src').replace("open","close") );
                                        },
                            function(){
                                $(this).parent('.sideBoxHeader').next().slideDown();
                                var img = $(this);
                                img.attr('src',img.attr('src').replace("close","open") );
                                        })
})
