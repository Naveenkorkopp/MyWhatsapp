

var roomName = js_tag;
    console.log("naveen : "+window.location.host);
    console.log("naveen1 : "+roomName);


var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + roomName + '/');


document.addEventListener("DOMContentLoaded", function(){

      chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

      chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var message = data['message'];
            document.querySelector('#chat-log').value += ('>>'+message + '\n');
            // var mychatdiv = document.querySelector('#chat_log_div');
            
            // for (var i = 0; i < data['chat_models'].length; i++) {
            //      mychatdiv.innerHTML += (data['chat_models'][i].chat_group_name + ' - - - > ');
            //      mychatdiv.innerHTML += (data['chat_models'][i].chat_log + '<br/>');
            // }

        };

        document.querySelector('#chat-message-input').focus();

        document.querySelector('#chat-message-submit').onclick = function(e) {
            var messageInputDom = document.querySelector('#chat-message-input');
            var message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));

            messageInputDom.value = '';
        };


        

        var input = document.getElementById("chat-message-input");
        
        input.addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                document.getElementById("chat-message-submit").click();
                document.getElementById("chat-log").scrollTop = document.getElementById("chat-log").scrollHeight;
            }
        });

});

    