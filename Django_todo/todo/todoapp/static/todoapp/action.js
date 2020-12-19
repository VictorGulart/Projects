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

    function get_data(taskId, content){
        // Raw AJAX call to get the data and form
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('get_modal/'+taskId, url);
        xhr.open('GET', url, true);

        xhr.onload = function(){
            if (xhr.status >= 200 && xhr.status < 400){
                content.innerHTML = xhr.responseText;
            }
        }

        xhr.onloadend = () => {
            document.getElementById('form-btn').onclick = () =>{
                update_task(taskId);
            }
        };

        xhr.send();
    }

    function edit_modal(taskId){
        // This functions shows the modal and get the data from server with XMLHttpRequest (Raw Ajax)
        var modal = document.getElementById('editModal');
        var content = document.getElementById('content');
       
        // Ajax call
        get_data(taskId, content);
        
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

    function update_task(taskId){
        // Handles the editing of a task on the modal 'pop up' 
        var xhr = new XMLHttpRequest();
        var url = new URL('edit_modal_task/'+taskId, window.location.href);

        xhr.open('POST', url, true);

        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 400){
                update_list();
            }
        }

        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN);

        // Get form data
        var formData = new URLSearchParams(new FormData(document.getElementById('modal-form')));
        xhr.send(formData);
    }

    function updateCheckbox(taskId, boxValue){
        var old_box = document.getElementById('checkbox'+taskId); // going to be replaced
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('checkbox/'+taskId, url);
        xhr.open('POST', url, true);

        xhr.onload = () =>{
            if (xhr.responseText == 'Success'){
                if (boxValue == false){
                    old_box.removeAttribute('cheked');
                }else{
                    old_box.setAttribute('checked', true);
                }
            
            } else{
                console.log('Something went wrong');
            }
            
        }
        
        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN);
        xhr.send()
    }
    
    function checkAllBoxes(){
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('check_all/', url);
        xhr.open('POST', url, true);

        xhr.onloadend = () =>{
            if (xhr.responseText == 'Success'){
                update_list(); // update the user's task list
            }   
        }
        
        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN);
        xhr.send()
    }

    function deleteAllChecked(){
        var xhr = new XMLHttpRequest();
        var url = window.location.href;
        url = new URL('delete_all_checked/', url);
        xhr.open('POST', url, true);

        xhr.onloadend = () =>{
            if (xhr.responseText == 'Success'){
                update_list(); // update the user's task list
            }   
        }
        
        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN);
        xhr.send()
    } 