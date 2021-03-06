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
        button_function($("#temp-setpoint-input"), "/set-temp-setpoint", "Error updating temperature setpoint");
    });
    $("#rh-setpoint").button().click(function(){
        button_function($("#rh-setpoint-input"), "/set-rh-setpoint", "Error updating humidity setpoint");
    });
    $("#temp-alarm-delta-set").button().click(function(){
        button_function($("#temp-alarm-delta-input"), "/set-temp-alarm-point", "Error updating temperature alarm threshold");
    });
    $("#rh-alarm-delta-set").button().click(function(){
        button_function($("#rh-alarm-delta-input"), "/set-rh-alarm-point", "Error updating humidity alarm threshold");
    });
    $("input[name='auto-temp']").on("change", function(){
        button_function($("input[name='auto-temp']:checked"), "/set-temp-ctl", "Error updating temperature control");
    });
    $("input[name='auto-rh']").on("change", function(){
        button_function($("input[name='auto-rh']:checked"), "/set-rh-ctl", "Error updating humidity control");
    });
    $("input[name='fan-state']").on("change", function(){
        button_function($("input[name='fan-state']:checked"), "/set-fan-state", "Error updating fan state");
    });
    $("input[name='fridge-state']").on("change", function(){
        button_function($("input[name='fridge-state']:checked"), "/set-fridge-state", "Error updating fridge state");
    });
    $("input[name='ctl-alg']").on("change", function(){
        button_function($("input[name='ctl-alg']:checked"), "/set-ctl-alg", "Error updating control algorithm");
    });
    init_state();
});

function set_status_bar(elem, current_val, max_val) {
    var percent = current_val / max_val * 100;
    $(elem).css("width", percent + "%");
}

function button_function(elem, url, error_msg){
    var new_val = $(elem).val();
    var args = {new_state: new_val};
    $.get( url, args )
    .done(function(result) {
        if (result === false) {
            $("#general-error-banner").text(error_msg);
            $("#general-error-banner").show();
        }
    })
};

function init_state(){
    $.get("/get-device-state").done(function(new_state) {
        // Alerts
        if (new_state.temp_alarm === "1") {
            $("#temp-alert-banner").show();
        }
        if (new_state.rh_alarm === "1") {
            $("#rh-alert-banner").show();
        }
        if (new_state.door_state === "1") {
            $("#door-alert-banner").show();
        }
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
        set_status_bar($("#fridge-temp"), parseFloat(new_state.fridge_temp), 20.0);

        $("#fridge-rh").text(parseFloat(new_state.fridge_rh).toFixed(0) + " %");
        set_status_bar($("#fridge-rh"), parseFloat(new_state.fridge_rh), 100.0);

        $("#external-temp").text(parseFloat(new_state.external_temp).toFixed(1) + " ˚C");
        set_status_bar($("#external-temp"), parseFloat(new_state.external_temp), 45.0);

        if (new_state.temp_control === "1"){
            $("#temp-ctl-on").addClass("active");
            $("#temp-ctl-off").removeClass("active");
            $("#temp-ctl-on-input").prop("checked", true);
        } else {
            $("#temp-ctl-off").addClass("active");
            $("#temp-ctl-on").removeClass("active");
            $("#temp-ctl-off-input").prop("checked", true);
        }
        if (new_state.rh_control === "1"){
            $("#rh-ctl-on").addClass("active");
            $("#rh-ctl-off").removeClass("active");
            $("#rh-ctl-on-input").prop("checked", true);
        } else {
            $("#rh-ctl-off").addClass("active");
            $("#rh-ctl-on").removeClass("active");
            $("#rh-ctl-off-input").prop("checked", true);
        }
        if (new_state.fan_state === "1"){
            $("#fan-ctl-on").addClass("active");
            $("#fan-ctl-off").removeClass("active");
            $("#fan-ctl-on-input").prop("checked", true);
        } else {
            $("#fan-ctl-off").addClass("active");
            $("#fan-ctl-on").removeClass("active");
            $("#fan-ctl-off-input").prop("checked", true);
        }

        $("#temp-setpoint-input").attr("placeholder", parseFloat(new_state.fridge_temp_setpoint).toFixed(1));
        $("#rh-setpoint-input").attr("placeholder", parseFloat(new_state.fridge_rh_setpoint).toFixed(0));

        if (new_state.control_algorithm === "basic"){
            $("#control-alg-basic").addClass("active");
            $("#control-alg-basic-input").prop("checked", true);
            $("#control-alg-pid").removeClass("active");
            $("#control-alg-learn").removeClass("active");
        } else if (new_state.control_algorithm === "pid"){
            $("#control-alg-pid").addClass("active");
            $("#control-alg-pid-input").prop("checked", true);
            $("#control-alg-basic").removeClass("active");
            $("#control-alg-learn").removeClass("active");
        } else if (new_state.control_algorithm === "learn"){
            $("#control-alg-learn").addClass("active");
            $("#control-alg-learn-input").prop("checked", true);
            $("#control-alg-basic").removeClass("active");
            $("#control-alg-pid").removeClass("active");
        } else {
            $("#control-alg-pid").removeClass("active");
            $("#control-alg-basic").removeClass("active");
            $("#control-alg-learn").removeClass("active");
        }
        if (new_state.fridge_state === "1"){
            $("#manual-fridge-ctl-on").addClass("active");
            $("#manual-fridge-ctl-on-input").prop("checked", true);
            $("#manual-fridge-ctl-off").removeClass("active");
        } else {
            $("#manual-fridge-ctl-off").addClass("active");
            $("#manual-fridge-ctl-off-input").prop("checked", true);
            $("#manual-fridge-ctl-on").removeClass("active");
        }
        $("#temp-alarm-delta-input").attr("placeholder", parseFloat(new_state.temp_alarm_delta).toFixed(1));
        $("#rh-alarm-delta-input").attr("placeholder", parseFloat(new_state.rh_alarm_delta).toFixed(0));
    })
}