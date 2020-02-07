// AWS DETAILS
AWS.config.region = 'us-east-1';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: "us-east-1:c5c3c75d-ae13-46c5-9f5a-a6585da63e59",
});
var lexruntime = new AWS.LexRuntime();

// CHATBOT DETAILS
var chatbotName = "greenkart_smart_assistant";
var chatbotVersion = '$LATEST';

// CREATE UNIQUE USER ID
var lexUserId = 'user' + Date.now();

// SESSION ATTRIBUTES
var sessionAttributes = {};

//WHEN USER CLICKS SEND
function pushChat(){
    
    // IF THERE IS SOMETHING TO BE SENT
    var inputText = document.getElementById('btn-input');
    if (inputText && inputText.value && inputText.value.trim().length > 0){
        var inputString = inputText.value.trim();
        timestamp = findTimeStamp();

        // SHOW MESSAGE SENT TO USER
        showDataSent(inputString, timestamp);

        // FORMING DATA TO BE SENT
        var params = {
            botAlias: chatbotVersion,
            botName: chatbotName,
            inputText: inputString,
            userId: lexUserId,
            sessionAttributes: sessionAttributes
        };

        // SENDING THE DATA TO LEX RUNTIME USING API
        lexruntime.postText(params, function(err, data){
            timestamp = findTimeStamp();
            
            // ERROR THROWN FROM API
            if(err){
                console.log(err, err.stack);
                data = {
                    "message" : "Something went wrong, please try again."
                }
                showDataReceived(data, timestamp);
            }

            // DATA RECEIVED ON SUCCESSFUL RUN OF API
            if(data){
                console.log(data);
                
                // UPDATE SESSION ATTRIBUTES
                sessionAttributes = data.sessionAttributes;

                // SHOW MESSAGE SENT
                showDataReceived(data, timestamp);
            }
            inputText.value = '';
        });
    }
}


function showDataSent(daText, timestamp){

    // CONVERSATION LIST
    var conversationDiv = document.getElementById('chatID');

    // NEW ITEM IN THE LIST
    var requestList = document.createElement("li");
    requestList.className = 'clearfix left';

    // NEW DIV CONTAINING MESSAGE AND TIME
    var requestDiv = document.createElement("div");
    requestDiv.className = "clearfix pull-left";

    // MESSAGE
    var requestPara = document.createElement("p");
    requestPara.className = 'message_sent';
    requestPara.appendChild(document.createTextNode(daText));

    // TIME
    var requestSmall = document.createElement("small");
    requestSmall.className = 'timestamp';
    requestSmall.appendChild(document.createTextNode(timestamp));

    // POPULATING
    requestDiv.appendChild(requestPara);
    requestDiv.appendChild(requestSmall);
    requestList.appendChild(requestDiv);
    conversationDiv.appendChild(requestList);
}

function showDataReceived(lexResponse, timestamp){
    
    // CONVERSATION LIST
    var conversationDiv = document.getElementById('chatID');

    // NEW ITEM IN THE LIST
    var requestList = document.createElement("li");
    requestList.className = 'clearfix right';

    // NEW DIV CONTAINING MESSAGE AND TIME
    var requestDiv = document.createElement("div");
    requestDiv.className = "clearfix pull-right";

    // MESSAGE
    var requestPara = document.createElement("p");
    requestPara.className = 'message_received';
    requestPara.appendChild(document.createTextNode(lexResponse.message));

    // IF THERE IS RESPONSE CARD 
    if(lexResponse.responseCard){
        var buttons_list = lexResponse.responseCard.genericAttachments[0].buttons;
        requestPara.appendChild(document.createElement('br'));

        // FOR EACH ENTRY IN THE BUTTONS LIST
        for(var i in buttons_list){
            var button_text = buttons_list[i].text;
            // var button_value = buttons_list[i].value;
            var button =  document.createElement("button");
            button.className = "btn rc_button";
            button.appendChild(document.createTextNode(button_text));
            button.setAttribute("onClick", "responseCardClick('" + button_text.toString() + "')");
            requestPara.appendChild(button);
            requestPara.appendChild(document.createElement('br'));
        }
    }

    // TIME
    var requestSmall = document.createElement("small");
    requestSmall.className = 'timestamp pull-right';
    requestSmall.appendChild(document.createTextNode(timestamp));

    // POPULATING
    requestDiv.appendChild(requestPara);
    requestDiv.appendChild(requestSmall);
    requestList.appendChild(requestDiv);
    conversationDiv.appendChild(requestList);
}

function responseCardClick(inputString){
    console.log(inputString);
    timestamp = findTimeStamp();

    // SHOW MESSAGE SENT TO USER
    showDataSent(inputString, timestamp);

    // FORMING DATA TO BE SENT
    var params = {
        botAlias: chatbotVersion,
        botName: chatbotName,
        inputText: inputString,
        userId: lexUserId,
        sessionAttributes: sessionAttributes
    };

    // SENDING THE DATA TO LEX RUNTIME USING API
    lexruntime.postText(params, function(err, data){
        timestamp = findTimeStamp();
        
        // ERROR THROWN FROM API
        if(err){
            console.log(err, err.stack);
            data = {
                "message" : "Something went wrong, please try again."
            }
            showDataReceived(data, timestamp);
        }

        // DATA RECEIVED ON SUCCESSFUL RUN OF API
        if(data){
            console.log(data);
            
            // UPDATE SESSION ATTRIBUTES
            sessionAttributes = data.sessionAttributes;

            // SHOW MESSAGE SENT
            showDataReceived(data, timestamp);
        }

    });
}

// GENERATE TIMESTAMP
function findTimeStamp(){
    date = new Date();
    hours = date.getHours();
    minutes = date.getMinutes();
    seconds = date.getSeconds();
    timestamp = hours + ":" + minutes + ":" + seconds;
    return timestamp;
}

//ENABLE SEND ON PRESS OF ENTER
window.addEventListener("keyup", function(event) {
    if (event.keyCode === 13 && document.activeElement.id == "btn-input") {
        document.getElementById("btn-chat").click();
    }
});

// MINMIZE MAXIMIZE CHAT WINDOW
function minMax(){
    console.log("Clicked");
    var chat_window = document.getElementById('chat-window');
    var panel_primary = document.getElementById('panel-primary');
    
    // MAXIMIZE
    if(chat_window.style.display=="none"){
        chat_window.style.display = "block";
        panel_primary.style.height = "500px";
    }
    // MINIMIZE
    else{
        chat_window.style.display = "none";
        panel_primary.style.height = "40px";
    }
    
}