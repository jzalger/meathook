/*
The basic control is a simple controller which triggers based on a single setpoint.
*/
#if defined(SPARK)
  #include "application.h"
#else
  #include "WProgram.h"
#endif

#include "basic_control.h"

BasicControl::BasicControl(double* current_value, double *target)
{
    current_value_ptr = current_value;
    target_ptr = target;
}

bool BasicControl::compute_action() {  // Returns action (true = cool, false = nothing)
    double _current_value = *current_value_ptr;
    double _target = *target_ptr;

    if (_current_value > _target) {
        return true;
    } else if (_current_value <= _target) {
        return false;
    } else {
        return false;
    }
}
