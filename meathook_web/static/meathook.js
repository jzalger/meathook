$(document).ready(function(){
    var base_url = "localhost:5000"

    $("#temp-setpoint").button().click(function(){
        var new_val = $("%temp-setpoint-input").val();
        var args = {new_state: new_val};
        $.get( "$base_url/set-temp-setpoint", args )
        .done(function(result) {
            if (result == 1) {
                $("#temp-setpoint-input").prop("placeholder", new_val);
            }
        })
    });

    $("#rh-setpoint").button().click(function(){

    });
    $("#temp-alarm-set").button().click(function(){

    });

    $("#rh-alarm-set").button().click(function(){

    });

    // Radio config
    $("input[type='button']").click(function(){
        var value = $("input[name='auto-temp']:checked").val();
        if(value == "ON"){
            // Turn on temp control
        } else {
            // Turn off temp control
        }
    });
    $("input[type='button']").click(function(){
        var value = $("input[name='auto-rh']:checked").val();
        if(value == "ON"){
            // Turn on temp control
        } else {
            // Turn off temp control
        }
    });
    $("input[type='button']").click(function(){
        var value = $("input[name='fan-state']:checked").val();
        if(value == "ON"){
            // Turn on temp control
        } else {
            // Turn off temp control
        }
    });
        $("input[type='button']").click(function(){
        var value = $("input[name='fridge-state']:checked").val();
        if(value == "ON"){
            // Turn on temp control
        } else {
            // Turn off temp control
        }
    });
    $("input[type='button']").click(function(){
        var value = $("input[name='ctl-alg']:checked").val();
        if(value == "Basic"){

        } else if (value == "PID") {

        } else if (value == "Learning") {

        }
    });
}
