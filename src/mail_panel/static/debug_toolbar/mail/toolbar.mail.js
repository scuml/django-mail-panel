function djmail_document_ready(f){
  if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
    f();
  } else {
    document.addEventListener('DOMContentLoaded', f);
  }
}

function djmail_load(url, element, callback)
{
    req = new XMLHttpRequest();
    req.open("GET", url, true);
    req.onload = function () {
        element.innerHTML = this.response;
        callback();
    };
    req.send();
}

djmail_document_ready(function(){

    window.onresize = resize_message;

    var $q = document.querySelector.bind(document);
    var $qa = document.querySelectorAll.bind(document);

    function resize_message() {
        new_height = window.innerHeight - $q("#djm_message_container").getBoundingClientRect().top + window.scrollY + window.pageYOffset -10
        $q("#djm_message_container").style.height = new_height + "px";
        preview_height = new_height - $q("#djm_message_overview").style.height - 10;
        $q("#djm_message_preview").style.height = preview_height;
    }

    function update_count(){
        unread_text = '';
        unread_count = $qa(".djm-unread").length;
        if (unread_count > 1)
            unread_text = unread_count + " unread messages";
        else if (unread_count == 1)
            unread_text = "1 unread message";
        sidebar_textbox = $q('.MailToolbarPanel small');
        if (sidebar_textbox)
            sidebar_textbox.innerHTML = unread_text;
    }
    function load_message(element){
        message_id = element.id;
        url = element.getAttribute('url');
        $qa('.djm-mail-toolbar tr.selected').forEach(function(e) {
            e.classList.remove('selected')
        });

        element.classList.add('selected');
        unread_marker = element.querySelector('.djm-unread');
        if(unread_marker)
            unread_marker.remove()

        update_count();

        djmail_load(url, $q('#djm_message_overview'), function(){

            // Animate in
            if($q('#djm_message_container').style.opacity == 0){
                resize_message();
                $q('#djm_message_container').style.opacity = 1;
            }

            // Display the last multipart message
            display_multipart($q(".djm-multipart-tabs span:last-child"));

            $qa(".djm-multipart-tab").forEach(function(e){
                e.addEventListener('click', function(){
                    display_multipart(this);
                })
            });
        });
    }
    var cache = {}
    function display_multipart(multipart_tab){
        url = multipart_tab.getAttribute('url');
        if(!url)
            return;

        $qa('.djm-multipart-tab-select').forEach(function(e) {
            e.classList.remove('djm-multipart-tab-select')
        });

        multipart_tab.classList.add('djm-multipart-tab-select')

        if (cache[url] != null){
            $q("#djm_message_preview iframe").contentDocument.querySelector('html').innerHTML= cache[url];
            return;
        }

        var request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.setRequestHeader("HTTP_X_REQUESTED_WITH", "ajax");

        request.onload = function() {
          if (request.status >= 200 && request.status < 400) {
            // Success!
            data = request.responseText;
            cache[url] = data;
            $q("#djm_message_preview iframe").contentDocument.querySelector('html').innerHTML = data;
          }
        };

        request.send();

    }

    $qa(".djm-message-row").forEach(function(e){
        e.addEventListener('click', function(){
            load_message(this);
        })
    });

});
