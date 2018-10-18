function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var pin2 = {"number":"2","state":false}
var pin4 = {"number":"4","state":false}
var pin12 = {"number":"12","state":false}

$("#pin2").click(
    function(){
        pin2["state"]= !pin2["state"]
        console.log(pin2["state"])
        sendData(pin2)
}
)
$("#pin4").click(
    function(){
        pin4["state"]= !pin4["state"]
        console.log(pin4["state"])
        sendData(pin4)
}
)

$("#pin12").click(
    function(){
        pin12["state"]= !pin12["state"]
        console.log(pin12["state"])
        sendData(pin12)
}
)


function sendData(data){
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/toggle-button", true);
    
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    
    xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 400) {
        let res_data = xhr.responseText;
        // * Converting data to js object
        let res = JSON.parse(res_data)
        console.log(`Worked: ${res['success']}`);
      
    } else {
        console.log('Lets try again');
    }
    }
    var data_to_post = JSON.stringify(data);
    xhr.send(data_to_post);
}
