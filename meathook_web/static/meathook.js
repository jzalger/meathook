$(document).ready(function(){
    $("#temp-alert-banner").hide();
    $("#rh-alert-banner").hide();
    $("#door-alert-banner").hide();
    $("#general-error-banner").hide();
    $("#cooling-badge").hide();
    $("#rh-badge").hide();
    $("#fan-badge").hide();

    // Button Actions
    $("#temp-setpoint").button().click(function(){
        var new_val = $("#temp-setpoint-input").val();
        var args = {new_state: new_val};
        $.get( "/set-temp-setpoint", args )
        .done(function(result) {
            console.log(result);
            if (result === true) {
                $("#temp-setpoint-input").attr("placeholder", new_val);
            } else {
                $("#general-error-banner").text("Error updating temperature setpoint");
                $("#general-error-banner").show();
            }
        })
    });
    $("#rh-setpoint").button().click(function(){
        var new_val = $("#rh-setpoint-input").val();
        var args = {new_state: new_val};
        $.get( "/set-rh-setpoint", args )
        .done(function(result) {
            if (result === true) {
                $("#rh-setpoint-input").attr("placeholder", new_val);
            } else {
                $("#general-error-banner").text("Error updating humidity setpoint");
                $("#general-error-banner").show();
            }
        })
    });
    $("#temp-alarm-set").button().click(function(){

    });
    $("#rh-alarm-set").button().click(function(){

    });
    $("input[name='auto-temp']").on("change", function(){
        var new_val = $("input[name='auto-temp']:checked").val();
        var args = {new_state: new_val};
        $.get( "/set-temp-ctl", args )
        .done(function(result) {
            console.log(result);
            if (result === false) {
                $("#general-error-banner").text("Error updating temperature control");
                $("#general-error-banner").show();
            }
        })
    });
    $("input[name='auto-rh']").on("change", function(){
        var new_val = $("input[name='auto-rh']:checked").val();

    });
    $("input[name='fan-state']").on("change", function(){
        var new_val = $("input[name='fan-state']:checked").val();

    });
    $("input[name='fridge-state']").on("change", function(){
        var new_val = $("input[name='fridge-state']:checked").val();

    });
    $("input[name='ctl-alg']").on("change", function(){
        var new_val = $("input[name='ctl-alg']:checked").val();

    });

    init_state();
});

function init_state(){
    $.get("/get-device-state").done(function(new_state) {
        // Alerts
        if (new_state.temp_alarm === true) {
            $("#temp-alert-banner").show();
        }
        if (new_state.rh_alarm === true) {
            $("#rh-alert-banner").show();
        }
        // TODO: Add Door alert once added to the firmware

        // Current State
        if (new_state.fridge_state === "1"){
            $("#cooling-badge").toggle();
        }
        if (new_state.humidifier_state === "1"){
            $("#rh-badge").toggle();
        }
        if (new_state.fan_state === "1"){
            $("#fan-badge").toggle();
        }
        $("#fridge-temp").text(parseFloat(new_state.fridge_temp).toFixed(1) + " ˚C");
        $("#fridge-rh").text(parseFloat(new_state.fridge_rh).toFixed(0) + " %");
        $("#external-temp").text(parseFloat(new_state.external_temp).toFixed(1) + " ˚C");
        if (new_state.temp_control === true){
            $("#temp-ctl-on").addClass("active");
            $("#temp-ctl-off").removeClass("active");
        } else {
            $("#temp-ctl-off").addClass("active");
            $("#temp-ctl-on").removeClass("active");
        }
        if (new_state.rh_control === true){
            $("#rh-ctl-on").addClass("active");
            $("#rh-ctl-off").removeClass("active");
        } else {
            $("#rh-ctl-off").addClass("active");
            $("#rh-ctl-on").removeClass("active");
        }
        if (new_state.fan_state === "1"){
            $("#fan-ctl-on").addClass("active");
            $("#fan-ctl-off").removeClass("active");
        } else {
            $("#fan-ctl-off").addClass("active");
            $("#fan-ctl-on").removeClass("active");
        }
        $("#temp-setpoint-input").attr("placeholder", parseFloat(new_state.fridge_temp_setpoint).toFixed(1));
        $("#rh-setpoint-input").attr("placeholder", parseFloat(new_state.fridge_rh_setpoint).toFixed(0));
        if (new_state.control_algorithm === "basic"){
            $("#control-alg-basic").addClass("active");
            $("#control-alg-pid").removeClass("active");
            $("#control-alg-learn").removeClass("active");
        } else if (new_state.control_algorithm === "pid"){
            $("#control-alg-pid").addClass("active");
            $("#control-alg-basic").removeClass("active");
            $("#control-alg-learn").removeClass("active");
        } else if (new_state.control_algorithm === "learn"){
            $("#control-alg-learn").addClass("active");
            $("#control-alg-basic").removeClass("active");
            $("#control-alg-pid").removeClass("active");
        } else {
            $("#control-alg-pid").removeClass("active");
            $("#control-alg-basic").removeClass("active");
            $("#control-alg-learn").removeClass("active");
        }
        if (new_state.fridge_state === "1"){
            $("#manual-fridge-ctl-on").addClass("active");
            $("#manual-fridge-ctl-off").removeClass("active");
        } else {
            $("#manual-fridge-ctl-off").addClass("active");
            $("#manual-fridge-ctl-on").removeClass("active");
        }
        $("#temp-alarm-delta-input").attr("placeholder", parseFloat(new_state.temp_alarm_delta).toFixed(1));
        $("#rh-alarm-delta-input").attr("placeholder", parseFloat(new_state.temp_alarm_delta).toFixed(0));
    })
}