var focusedId = 1;


function crossIt(obj, taskId){
    // arg here is the tag itself
    //console.log(obj.checked);
    var task = document.getElementById(taskId)
    if (obj.checked == true){
        task.style.textDecoration = 'line-through';
    } else{
        task.style.textDecoration = 'none';
    }
}



function getData(taskId) {

    // update the focusedId variable
    focusedId = taskId;
    console.log(focusedId);
    
   // this function should call Django and get the data and display it on the page 
   // makes a request to the server django is going to return the data within 
    let xhr = new XMLHttpRequest();
    let current = window.location.href; // gets the current url
    let url = new URL(current); // create the urls string to add to the current url
    url.searchParams.append('key', taskId);

    // open the connection
    xhr.open('GET', url.toString());

    // handle the response
    xhr.onload = function (){
        if (xhr.status >= 200 && xhr.status < 400){
            // if the response is OK

            let text = JSON.parse(xhr.responseText);
            document.getElementById('id_title').value = text[0];
            document.getElementById('editor').value = text[1];
        }
    }
    // send the request
    xhr.send();

}


// function delete_task(taskId){
//     // add a pop up here to make sure the user wants to delete it 
//     let xhr = new XMLHttpRequest();
//     let url = window.location.href;
//     // url = new URL(url + 'deletepage');
//     url = new URL(url);
//     url.searchParams.append('key', taskId);
//     xhr.open('DELETE', url.toString());
//     console.log(url.toString());

//     // handle response
//     xhr.onload = function (){
//         if (xhr.status >= 200 && xhr.status <400){
//             console.log('All done');
//         }
//     }

//     // send the request
//     xhr.send();
// }

function clearForm(){
        document.getElementById('id_title').value = '';
        document.getElementById('editor').value = '';
        focusedId = 0;
        console.log('New Task to be Added')
}