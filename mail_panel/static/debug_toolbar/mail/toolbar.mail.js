function djmail_document_ready(f){
    if (document.readyState !== 'loading') {
        f();
    } else {
        document.addEventListener('DOMContentLoaded', f);
    }
}

function djmail_get(url, callback)
{
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            try {
                var data = JSON.parse(req.responseText);
            } catch(err) {
                console.log(err.message + " in " + req.responseText);
                return;
            }
            callback(data);
        }
    };
    req.open("GET", url, true);
    req.send();
}

function djmail_load(url, element, callback)
{
    var req = new XMLHttpRequest();
    req.open("GET", url, true);
    req.onload = function () {
        element.innerHTML = this.response;
        callback();
    };
    req.send();
}

djmail_document_ready(function(){

    var $q = document.querySelector.bind(document);
    var $qa = document.querySelectorAll.bind(document);

    window.onresize = resize_message;

    window.mail_panel_settings = {}

    // resize on message list css resize
    let observer = new MutationObserver(function(mutations) {
      resize_message()
    });
    let child = $q('.djm-message-list');
    if(child){
        observer.observe(child, { attributes: true });
    }

    function resize_message() {
        let new_height = window.innerHeight - $q("#djm_message_container").getBoundingClientRect().top + window.scrollY + window.pageYOffset -10
        $q("#djm_message_container").style.height = new_height + "px";
        let preview_height = new_height - $q("#djm_message_overview").style.height - 10;
        $q("#djm_message_preview").style.height = preview_height;
    }

    function update_count(){
        var unread_text = '';
        var unread_count = $qa(".djm-unread").length;
        if (unread_count > 1)
            unread_text = unread_count + " unread messages";
        else if (unread_count == 1)
            unread_text = "1 unread message";
        var sidebar_textbox = $q('.MailToolbarPanel small');
        if (sidebar_textbox)
            sidebar_textbox.innerHTML = unread_text;
    }

    function clear_message(url){
        djmail_get(url, function(data){
            if(data["status"] != "success"){
                return
            }
            $q("#djm_message_table tbody tr [url='"+ url +"']").closest("tr").remove();
            $q('#djm_message_container').style.opacity = 0;
            resize_message();
        })


    }
    window.mail_panel_settings["clear_message"] = clear_message

    function clear_all_messages(url){
        var confirm = window.confirm("Are you sure you want to clear all messages?");
        if (confirm == false) {
            return
        }
        djmail_get(url, function(data){
            if(data["status"] != "success"){
                return
            }
            $qa("#djm_message_table tbody tr").forEach(el => el.remove());
            $q('#djm_message_container').style.opacity = 0;
            resize_message();
        })
    }
    window.mail_panel_settings["clear_all_messages"] = clear_all_messages


    function load_message(element){
        let message_id = element.id;
        let url = element.getAttribute('url');
        $qa('.djm-mail-toolbar tr.selected').forEach(function(e) {
            e.classList.remove('selected')
        });

        element.classList.add('selected');
        let unread_marker = element.querySelector('.djm-unread');
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
        let url = multipart_tab.getAttribute('url');
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
            let data = request.responseText;
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
    $qa("[jsmethod]").forEach(function(e){
        e.addEventListener('click', function(e){
            e.stopPropagation(); // stop row onClick event
            var method = window.mail_panel_settings[this.getAttribute("jsmethod")]
            method(this.getAttribute("url"))

        })

    })
});
