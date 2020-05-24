$(document).ready(function(){
    $("#temp-setpoint").button().click(function(){

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
