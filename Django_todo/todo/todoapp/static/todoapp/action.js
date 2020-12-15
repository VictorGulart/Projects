var focusedId = 1;



    function update_list(){
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('list', url);
        xhr.open('GET', url, true);

        xhr.onload = function(){
            if (xhr.status >= 200 && xhr.status < 400){
                document.getElementById('list').innerHTML = xhr.responseText;
            }
        }
        // Send proper header information
        xhr.send();
    }

    function delete_task(taskId){
        console.log('Inside POST request');
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL(taskId + '/delete/', url);
        xhr.open('POST', url, true);

        xhr.onload = function(){
            if (xhr.status >= 200 && xhr.status < 400){
                document.getElementById('list').innerHTML = xhr.responseText;
            }
        }
        // Send proper header information
        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN)
        xhr.send();
    }

    function add_task(){
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('/add_task', url);
        xhr.open('POST', url, true);
        xhr.onload = function(){
            if (xhr.status >= 200 && xhr.status < 400){
                document.getElementById('list').innerHTML = xhr.responseText;
            }
        }
        // Send proper header information
        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN)
        xhr.send();
    }

    function open_task(n){
        elm = document.getElementById(n);
        elm.classList.toggle('show');
    }

    function check_task(n){
        elm = document.getElementById("checkbox" + n);
        if (elm.checked == false){
            elm.checked = true;
        }else{
            elm.checked = false;
        } 
    }

    function edit_modal(taskId){
        var modal = document.getElementById('editModal');
        var content = document.getElementById('content');
        
        // AJAX
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('edit_modal/'+taskId, url);

        xhr.open('POST', url, true);

        xhr.onload = function(){
            if (xhr.status >= 200 && xhr.status < 400){
                content.innerHTML = xhr.responseText;
                // update_list();
            }
        }

        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN);
        xhr.send();

        // Display the Modal
        modal.style.display = 'block';
        var closeBtn = document.getElementsByClassName('close')[0];
        closeBtn.onclick = function(){
            modal.style.display = 'none';
        }

        modal.onclick = function(){
            modal.style.display = 'none';
        }

        content.onclick = function(e){
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            return false;
        }

    }
