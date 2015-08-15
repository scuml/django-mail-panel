(function ($) {

    window.onresize = resize_message;

    function resize_message() {
        new_height = window.innerHeight - $("#djm_message_container").offset().top + $(document).scrollTop() - 50;
        $("#djm_message_container").height(new_height);
        new_height = new_height - $("#djm_message_overview").height() - 10;
        $("#djm_message_preview").height(new_height);
    }
    function update_count(){
        unread_text = '';
        unread_count = $(".djm-unread:visible").length;
        if (unread_count > 1)
            unread_text = unread_count + " unread messages";
        else if (unread_count == 1)
            unread_text = "1 unread message";
        $('.MailToolbarPanel small').html(unread_text)
    }
    function load_message(element){

        message_id = $(element).attr('id');
        url = $(element).attr('url');
        $('.djm-mail-toolbar tr').removeClass('selected');
        $('#'+message_id).addClass('selected');
        $('#'+message_id).find('.djm-unread').hide();

        update_count();

        $('#djm_message_overview').load(url, function(){

            // Animate in
            if($('#djm_message_container').css('opacity')==0){
                resize_message();

                $('#djm_message_container').css('marginTop', "-=20");

                $('#djm_message_container').animate({
                  marginTop: "+=20",
                  opacity: 1
                });
            }

            display_multipart($("#djm_message_overview span:last"));
            $("#djm_message_overview span").click(function(){
                display_multipart(this);
            })
        })
    }
    var cache = {}
    function display_multipart(span){
        url = $(span).attr('url');
        if(!url)
            return;

        $(".djm-multipart-tab-select").removeClass('djm-multipart-tab-select');
        $(span).addClass('djm-multipart-tab-select')
        console.info(url);
        if (cache[url] != null){
            $("#djm_message_preview iframe").contents().find('html').html(cache[url]);
            return;
        }
        $.ajax({
            type: "GET",
            url: url,
            beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "ajax");},
            success: function(data){
                cache[url] = data;
                //$("#"+iframe).attr('src',"/")
                $("#djm_message_preview iframe").contents().find('html').html(data);
            }
        });
    }

    $(".djm-message-row").click(function(){
        load_message(this);
    })

})(djdt.jQuery);