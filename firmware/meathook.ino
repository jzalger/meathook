// MeatHook
// J. Zalger - 2020
#include <SHT1x.h>
#include <pid.h>
#include <string>
#include "basic_control.h"

#define REF_VOLTAGE 3.4  //Voltage reference for external temp sensor
#define SHT_SCK D1
#define SHT_DATA D0
#define HUMID_PIN D2
#define FAN_PIN D3
#define FRIDGE_PIN D4
#define LED_PIN D5
#define DOOR_SENS D6
#define EXT_TEMP_PIN A5

double external_temp = 0.0;
double fridge_temp = 0.0;
double fridge_rh = 0.0;

// Parameters for PID control
double temp_setpoint = 7.0;
double rh_setpoint = 40.0;
double temp_pid_output = 0.0;
double rh_pid_output = 0.0;
int pid_temp_window_size = 60000;   // Time in milliseconds
int pid_rh_window_size = 30000;     // Time in milliseconds
unsigned long pid_temp_window_start_time;
unsigned long pid_rh_window_start_time;

int compressor_protect_time = 300;  // Time in seconds
int last_fridge_action = -compressor_protect_time * 1000;

double temp_alarm_delta = 15.0;  //+- deg C from setpoint to trigger alarm
double rh_alarm_delta = 40.0;    //+= % from setpoint to trigger alarm

bool temp_control = TRUE;
bool rh_control = FALSE;
bool fan_state = FALSE;
bool fridge_state = FALSE;
bool humidifier_state = FALSE;
bool temp_alarm = FALSE;
bool rh_alarm = FALSE;
bool stream_data = TRUE;
bool door_state = FALSE;  // False = CLOSED
bool logging_mode = TRUE;

String main_state = "fridge_temp, fridge_rh, external_temp, fridge_state, humidifier_state, fan_state";
String aux_state = "temp_setpoint, rh_setpoint, temp_alarm, rh_alarm, control_alg, temp_alarm_threash, rh_alarm_threash";

int stream_interval = 1; // Stream update interval in minutes
unsigned long last_stream_update;
unsigned long last_alarm_message;

SHT1x fridge_sensor(SHT_DATA, SHT_SCK);

String control_algorithm = "basic";

// Note: These PID settings here are arbitrary
PID temp_pid(&fridge_temp, &temp_pid_output, &temp_setpoint, 2.0, 2.0, 1.0, PID::P_ON_M, PID::DIRECT);
PID rh_pid(&fridge_rh, &rh_pid_output, &rh_setpoint, 2.0, 2.0, 1.0, PID::P_ON_M, PID::DIRECT);

// Basic Control for temperature
BasicControl basic_temp_control(&fridge_temp, &temp_setpoint);

void setup() {
    pinMode(HUMID_PIN, OUTPUT);
    pinMode(FRIDGE_PIN, OUTPUT);
    pinMode(FAN_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);

    Particle.variable("humidifier_state", humidifier_state);
    Particle.variable("fridge_state", fridge_state);
    Particle.variable("external_temp", external_temp);
    Particle.variable("fridge_temp", fridge_temp);
    Particle.variable("fridge_rh", fridge_rh);
    Particle.variable("fridge_temp_setpoint", temp_setpoint);
    Particle.variable("fridge_rh_setpoint", rh_setpoint);
    Particle.variable("rh_control", rh_control);
    Particle.variable("temp_control", temp_control);
    Particle.variable("fan_state", fan_state);
    Particle.variable("temp_alarm", temp_alarm);
    Particle.variable("rh_alarm", rh_alarm);
    Particle.variable("temp_alarm_delta", temp_alarm_delta);
    Particle.variable("rh_alarm_delta", rh_alarm_delta);
    Particle.variable("control_algorithm", control_algorithm);

    Particle.function("set_temp_setpoint", set_temp_setpoint);
    Particle.function("set_rh_setpoint", set_rh_setpoint);
    Particle.function("set_control", set_control);
    Particle.function("set_temp_control", set_temp_control);
    Particle.function("set_rh_control", set_rh_control);
    Particle.function("set_stream_data", set_stream_data);
    Particle.function("set_stream_interval", set_stream_interval);
    Particle.function("set_temp_alarm_delta", set_temp_alarm_delta);
    Particle.function("set_rh_alarm_delta", set_rh_alarm_delta);
    Particle.function("set_fan_state", set_fan_state);
    Particle.function("set_fridge_state", set_fridge_state);
    Particle.function("set_control_algorithm", set_control_algorithm);

    if (control_algorithm == "pid"){
        temp_pid.SetOutputLimits(0, pid_temp_window_size);
        rh_pid.SetOutputLimits(0, pid_rh_window_size);
        temp_pid.SetMode(PID::AUTOMATIC);
        rh_pid.SetMode(PID::AUTOMATIC);
    }
}

void loop() {
    delay(1000); // Dont overdrive the system

    // Turn on lights if door opens
    manage_light();

    // Read sensors
    external_temp = (((analogRead(EXT_TEMP_PIN) * REF_VOLTAGE) / 4095.0) - 0.5) * 100;
    fridge_temp = fridge_sensor.readTemperatureC();
    fridge_rh = fridge_sensor.readHumidity();

    // Adjust system controls
    if (temp_control == TRUE) {
        if (control_algorithm == "pid"){
            temp_pid.Compute();
            unsigned long now = millis();
            if (now - pid_temp_window_start_time > pid_temp_window_size) {
                pid_temp_window_start_time += pid_temp_window_size;
            }
            if (temp_pid_output > now - pid_temp_window_start_time){
                start_fridge();
            } else {
                stop_fridge();
            }

        } else if (control_algorithm == "basic"){
            bool action = basic_temp_control.compute_action();
            if (action == TRUE){
                start_fridge();
            } else {
                stop_fridge();
            }
        }
    }

    /*
    if (rh_control == TRUE) {
        if (control_algorithm == "pid"){
            rh_pid.Compute();
            unsigned long now = millis();
            if (now - pid_rh_window_start_time > pid_rh_window_size) {
                pid_rh_window_start_time += pid_rh_window_size;
            }
            if (rh_pid_output > now - pid_rh_window_start_time){
                start_humidifier();
            } else {
                stop_humidifier();
            }
        }
    }
    */

    if (fan_state == TRUE) {
        start_fan();
    } else {
        stop_fan();
    }

    // Trigger any system alarms
    if (fridge_temp > temp_setpoint + temp_alarm_delta ||
        fridge_temp < temp_setpoint - temp_alarm_delta) {
            temp_alarm = TRUE;
            trigger_temp_alarm();
        } else {
            temp_alarm = FALSE;
        }
    if (fridge_rh > rh_setpoint + rh_alarm_delta ||
        fridge_rh < rh_setpoint - rh_alarm_delta) {
            rh_alarm = TRUE;
            trigger_rh_alarm();
        } else {
            rh_alarm = FALSE;
        }

    // Post readings to the cloud server
    if (stream_data == TRUE) {
        if ((millis() - last_stream_update) / 1000 > (stream_interval * 60)) {

            main_state = String(fridge_temp) + "," + String(fridge_rh) + "," + String(external_temp) + "," +
                String(fridge_state) + "," + String(humidifier_state) + "," + String(fan_state) + "," + String(door_state);

            aux_state = String(temp_setpoint) + "," +  String(rh_setpoint) + "," +  String(temp_alarm) + "," +
                String(rh_alarm) + "," + control_algorithm + "," + String(temp_alarm_delta) + "," + String(rh_alarm_delta)
                + "," + String(temp_control) + "," + String(rh_control);

            Particle.publish("main_state", main_state);
            Particle.publish("aux_state", aux_state);
            last_stream_update = millis();
        }
    }
}

void start_fridge(){
    int time_since_last_action = millis() - last_fridge_action;
    if (time_since_last_action >= compressor_protect_time * 1000){
        digitalWrite(FRIDGE_PIN, HIGH);
        fridge_state = TRUE;
    }
}

void stop_fridge(){
    digitalWrite(FRIDGE_PIN, LOW);
    if (fridge_state == TRUE) {
        last_fridge_action = millis();
    }
    fridge_state = FALSE;
}


void start_fan(){
    digitalWrite(FAN_PIN, HIGH);
    fan_state = TRUE;
}

void stop_fan(){
    digitalWrite(FAN_PIN, LOW);
    fan_state = FALSE;
}

void start_humidifier() {
    digitalWrite(HUMID_PIN, LOW);
    humidifier_state = TRUE;
}

void stop_humidifier(){
    digitalWrite(HUMID_PIN, HIGH);
    humidifier_state = FALSE;
}

void trigger_temp_alarm() {
    // TODO: Rate limit this with last_alarm variable
    Particle.publish("temp_alarm", "1");
}

void trigger_rh_alarm(){
    Particle.publish("rh_alarm", "1");
}

void manage_light(){
    door_state = digitalRead(DOOR_SENS);
    if (door_state == TRUE){
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }
}

int set_temp_setpoint(String arg){
    temp_setpoint = arg.toFloat();
    return 0;
}
int set_rh_setpoint(String arg){
    rh_setpoint = arg.toFloat();
    return 0;
}
int set_control(String arg){
    if (arg == "ON") {
        temp_control = TRUE;
        rh_control = TRUE;
        return 0;
    } else if (arg == "OFF"){
        temp_control = FALSE;
        rh_control = FALSE;
        return 0;
    } else {
        return -1;
    }
}
int set_temp_control(String arg){
    if (arg == "ON") {
        temp_control = TRUE;
        return 0;
    } else if (arg == "OFF"){
        temp_control = FALSE;
        return 0;
    } else {
        return -1;
    }
}

int set_rh_control(String arg){
    if (arg == "ON") {
        rh_control = TRUE;
        return 0;
    } else if (arg == "OFF"){
        rh_control = FALSE;
        return 0;
    } else {
        return -1;
    }
}
int set_fridge_state(String arg){
    if (arg == "ON") {
        start_fridge();
        return 0;
    } else if (arg == "OFF"){
        stop_fridge();
        return 0;
    } else {
        return -1;
    }
}

int set_stream_data(String arg){
    if (arg == "ON"){
        stream_data = TRUE;
        return 0;
    } else if (arg == "OFF"){
        stream_data = FALSE;
        return 0;
    } else {
        return -1;
    }
}
int set_stream_interval(String arg){
    stream_interval = arg.toInt();
    return 0;
}
int set_temp_alarm_delta(String arg){
    temp_alarm_delta = arg.toFloat();
    return 0;
}
int set_rh_alarm_delta(String arg){
    rh_alarm_delta = arg.toFloat();
    return 0;
}
int set_fan_state(String arg){
    if (arg == "ON") {
        start_fan();
        return 0;
    } else if (arg == "OFF") {
        stop_fan();
        return 0;
    } else {
        return -1;
    }
}
int set_control_algorithm(String arg){
    if (arg == "basic"){
        control_algorithm = "basic";
        return 0;
    } else if (arg == "pid") {
        control_algorithm = "pid";
        return 0;
    } else {
        return -1;
    }
}

