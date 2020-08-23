#include "funks.h"

#define s0_en A1
#define s0_step 11
#define s0_dir 12
#define s1_en A2
#define s1_step 9
#define s1_dir 10
#define servo_pin 4

// #define servo_pin 6
// #define button_in 5


Adafruit_NeoPixel pixel = Adafruit_NeoPixel(1, 8, NEO_GRB + NEO_KHZ800);

using namespace std;

struct stepper
{
  public:
  void init(int s_pin, int d_pin, int e_pin, bool reverse);
  void enable();
  void disable();
  void set_dir(bool dir);
  bool step_if_needed();
  void take_step();
  void overwrite_pos(int32_t newpos);
  void update_config(int32_t steps_per_rev_new);
  void set_rad_target(double target);
  void set_zero_rads(double rads);
  int32_t get_steps();
  float get_rads();

  private:
  bool current_dir = false;
  int step_pin;
  int dir_pin;
  int en_pin;
  int reverse;
  double target_rads = 0;
  int32_t step_count = 0;
  float steps_per_rev = 3200;
};

struct scara_bot
{
  public:
  void init(stepper step0, stepper step1, Servo servo_obj);
  void configure(float arm0_mm_new, float arm1_mm_new, float s0_spr_new, float s1_spr_new, float x0_off_new, float y0_off_new);
  void enable_motors(bool x, bool y);
  void disable_motors(bool x, bool y);
  void zero();
  void move_motor_linear(float x_target_mm, float y_target_mm, float v_max);
  void move_motor_arc(float x_target_mm, float y_target_mm, float ival, float jval, float v_max, bool cw);
  void set_def_speeds(float new_accel, float new_vel);
  void get_pos(float &xpos_mm, float &ypos_mm);

  void debug_print();

  private:
  stepper s0;
  stepper s1;
  float xpos_mm = 0;
  float ypos_mm = 0;
  Servo p_servo;

  float def_accel = 500;
  float def_vel = 6000;

  float arm0_mm = 100.5;
  float arm1_mm = 90;
  float x0_offset_mm = 25;
  float y0_offset_mm = 135;

  double cos_solve(float l1, float l2, float l3);
  void ik_solve(float xtar_mm, float ytar_mm);
};

struct gcode_command_floats
{
  gcode_command_floats(vector<string> inputs);

  public:
  float fetch(char com_key);
  bool com_exists(char com_key);

  private:
  vector<char> commands;
  vector<float> values;
};
