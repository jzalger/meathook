#ifndef basic_control_h
#define basic_control_h
#define LIBRARY_VERSION	0.1

class BasicControl
{
    public:
        BasicControl(double*, double*);

        bool compute_action();

    private:
        double *current_value_ptr;
        double *target_ptr;
};
#endif
