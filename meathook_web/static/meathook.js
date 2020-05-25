var base_url = "localhost:5000"

$(document).ready(function(){
    $("#temp-alert-banner").hide();
    $("#rh-alert-banner").hide();
    $("#door-alert-banner").hide();
    $("#cooling-badge").hide();
    $("#rh-badge").hide();
    $("#fan-badge").hide();

    // Button Actions
    $("#temp-setpoint").button().click(function(){
        var new_val = $("#temp-setpoint-input").val();
        var args = {new_state: new_val};
        jQuery.get( "/set-temp-setpoint", args )
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

    init_state();
});

function init_state(){
    jQuery.get("/get-device-state").done(function(new_state) {
        // Alerts
        if (new_state.temp_alarm === true) {
            $("#temp-alert-banner").show();
        }
        if (new_state.rh_alarm === true) {
            $("#rh-alert-banner").show();
        }
        // TODO: Add Door alert once added to the firmware

        // Current State
        if (new_state.fridge_state === true){
            $("#cooling-badge").toggle();
        }
        if (new_state.humidifier_state === true){
            $("#rh-badge").toggle();
        }
        if (new_state.fan_state === true){
            $("#fan-badge").toggle();
        }

    })
}