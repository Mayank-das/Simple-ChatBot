function getBotResponse(input) {
    const close = ["close", "quit", "exit"];
    //rock paper scissors
    if (input == "rock") {
        return "paper";
    } else if (input == "paper") {
        return "scissors";
    } else if (input == "scissors") {
        return "rock";
    }

    else if (input == "I Like It!"){
        return "It's my pleasure thank you!"
    }
    // Simple responses
    // if (input == "hello") {
    //     return "Hello there!";
    // } 
    else if (close.includes(input.toLowerCase())) {
        document.getElementById("chat-button").click();
        return "closed successfully!";
    } else {
        var res;
        $.ajax({
                url: "/predict",
                async: false,
                dataType: 'json',
                data: { usr: input},
                success: function(data){
                    res = data.chat;
                }
            });
        return res;
    }
}