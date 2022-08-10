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
    $("#temp-alarm-delta-set").button().click(function(){
        button_function($("#temp-alarm-delta-input"), "/set-temp-alarm-point", "Error updating temperature alarm threshold");
    });
    $("#rh-alarm-limit-set").button().click(function(){
        button_function($("#rh-alarm-limit-input"), "/set-rh-alarm-limit", "Error updating humidity alarm threshold");
    });
    $("input[name='auto-temp']").on("change", function(){
        button_function($("input[name='auto-temp']:checked"), "/set-temp-ctl", "Error updating temperature control");
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
    $("input[name='es-state']").on("change", function(){
        button_function($("input[name='es-state']:checked"), "/set-es-state", "Error updating energy saving state");
    });
    $("#overnight-temp-btn").button().click(function(){
        button_function($("#overnight-temp-input"), "/set-es-temp-setpoint", "Error updating energy saving setpoint");
    });
    $("#refresh-state-btn").button().click(function(){
        let error_msg = "Error refreshing device state";
        $.get( "/refresh-device-state", "" )
        .done(function(result) {
            if (result === false) {
                $("#general-error-banner").text(error_msg);
                $("#general-error-banner").show();
            } else {
                update_state(result);
            }
        })
    });
    $("#overnight-time-btn").button().click(function(){
        let time_dict = {"es_start_string":$("#overnight-time1-input").val(), "es_stop_string":$("#overnight-time2-input").val()};
        set_es_time(JSON.stringify(time_dict) , "/set-es-timing", "Error updating es-timing");
    });
    init_state();
    setInterval(init_state, 10000);
});

function set_status_bar(elem, current_val, max_val) {
    let percent = current_val / max_val * 100;
    $(elem).css("width", percent + "%");
}
function button_function(elem, url, error_msg){
    let new_val = $(elem).val();
    let args = {new_state: new_val};
    call_func(url, args, error_msg);
}
function set_es_time(times_dict, url, error_msg) {
    let args = {new_state: times_dict};
    call_func(url, args, error_msg);
}

function call_func(url, args, error_msg){
    $.get( url, args )
    .done(function(result) {
        if (result === false) {
            $("#general-error-banner").text(error_msg);
            $("#general-error-banner").show();
        }
    })
}

function init_state(){
    $.get("/get-device-state").done(function(new_state) {
        update_state(new_state);
    })
}

function update_state(new_state){
    // Alerts
    if (new_state.temp_alarm === true) {
        $("#temp-alert-banner").show();
    }
    if (new_state.rh_alarm === true) {
        $("#rh-alert-banner").show();
    }
    if (new_state.door_state === true) {
        $("#door-alert-banner").show();
    }
    // Current State
    if (new_state.fridge_state === true){
        $("#cooling-badge").toggle();
    }
    if (new_state.fan_state === true){
        $("#fan-badge").toggle();
    }

    $("#fridge-temp").text(parseFloat(new_state.fridge_temp).toFixed(1) + " ˚C");
    set_status_bar($("#fridge-temp"), parseFloat(new_state.fridge_temp), 20.0);

    $("#fridge-rh").text(parseFloat(new_state.fridge_rh).toFixed(0) + " %");
    set_status_bar($("#fridge-rh"), parseFloat(new_state.fridge_rh), 100.0);

    $("#external-temp").text(parseFloat(new_state.external_temp).toFixed(1) + " ˚C");
    set_status_bar($("#external-temp"), parseFloat(new_state.external_temp), 45.0);

    if (new_state.temp_control === true){
        $("#temp-ctl-on").addClass("active");
        $("#temp-ctl-off").removeClass("active");
        $("#temp-ctl-on-input").prop("checked", true);
    } else {
        $("#temp-ctl-off").addClass("active");
        $("#temp-ctl-on").removeClass("active");
        $("#temp-ctl-off-input").prop("checked", true);
    }
    if (new_state.fan_state === true){
        $("#fan-ctl-on").addClass("active");
        $("#fan-ctl-off").removeClass("active");
        $("#fan-ctl-on-input").prop("checked", true);
    } else {
        $("#fan-ctl-off").addClass("active");
        $("#fan-ctl-on").removeClass("active");
        $("#fan-ctl-off-input").prop("checked", true);
    }

    $("#temp-setpoint-input").attr("placeholder", parseFloat(new_state.temp_setpoint).toFixed(1));

    if (new_state.es_state === true){
        $("#energy-saving-on").addClass("active");
        $("#energy-saving-off").removeClass("active");
        $("#energy-saving-on-input").prop("checked", true);
    } else {
        $("#energy-saving-off").addClass("active");
        $("#energy-saving-on").removeClass("active");
        $("#energy-saving-off-input").prop("checked", true);
    }
    $("#overnight-temp-input").attr("placeholder", parseFloat(new_state.es_temp_setpoint).toFixed(1));
    $("#overnight-time1-input").attr("placeholder", new_state.es_start);
    $("#overnight-time2-input").attr("placeholder", new_state.es_stop);

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
    if (new_state.fridge_state === true){
        $("#manual-fridge-ctl-on").addClass("active");
        $("#manual-fridge-ctl-on-input").prop("checked", true);
        $("#manual-fridge-ctl-off").removeClass("active");
    } else {
        $("#manual-fridge-ctl-off").addClass("active");
        $("#manual-fridge-ctl-off-input").prop("checked", true);
        $("#manual-fridge-ctl-on").removeClass("active");
    }
    $("#temp-alarm-delta-input").attr("placeholder", parseFloat(new_state.temp_alarm_delta).toFixed(1));
    $("#rh-alarm-limit-input").attr("placeholder", parseFloat(new_state.rh_alarm_limit).toFixed(0));

    if (Object.entries(new_state).length > 0){
        $("#disconnected-badge").hide();
    }
}
