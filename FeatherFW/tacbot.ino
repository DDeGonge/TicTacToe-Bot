/* STEPPER STUFF */

void stepper::init(int s_pin, int d_pin, int e_pin, bool reverse)
{
  step_pin = s_pin;
  dir_pin = d_pin;
  en_pin = e_pin;
  pinMode(step_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(en_pin, OUTPUT);
  digitalWrite(en_pin, HIGH);
  digitalWrite(step_pin, LOW);
  digitalWrite(dir_pin, LOW);
  step_count = 0;
  if(reverse){
    reverse = -1;
  }
  else{
    reverse = 1;
  }
}

void stepper::enable()
{
  digitalWrite(en_pin, LOW);
}

void stepper::disable()
{
  digitalWrite(en_pin, HIGH);
}

void stepper::set_dir(bool dir)
{
  if(dir && !current_dir)
  {
    digitalWrite(dir_pin, HIGH);
    current_dir = true;
  }
  else if(!dir && current_dir)
  {
    digitalWrite(dir_pin, LOW);
    current_dir = false;
  }
}

void stepper::overwrite_pos(int32_t newpos)
{
  step_count = newpos;
}

void stepper::update_config(int32_t steps_per_rev_new)
{
  steps_per_rev = steps_per_rev_new;
}

void stepper::take_step()
{
  digitalWrite(step_pin, HIGH);
  delayMicroseconds(1);
  digitalWrite(step_pin, LOW);
  if(current_dir) step_count++;
  else step_count--;
}

float stepper::get_rads()
{
  return 2 * PI * step_count / steps_per_rev;
}

void stepper::set_zero_rads(double rads)
{
  step_count = steps_per_rev * rads / (2 * PI);
}

void stepper::set_rad_target(double target)
{
  target_rads = target;
}

bool stepper::step_if_needed()
{
  uint32_t step_target = (steps_per_rev * target_rads);
  step_target /= 2 * PI;

  if(step_target == step_count) return false;

  if(step_target > step_count)
  {
    set_dir(true);
  }
  else
  {
    set_dir(false);
  }

  take_step();
  return true;
}



/* SCARA BOT STUFF */

void scara_bot::init(stepper step0, stepper step1, Servo servo_obj)
{
  s0 = step0;
  s1 = step1;
  p_servo = servo_obj;
}

void scara_bot::configure(float arm0_mm_new, float arm1_mm_new, float s0_spr_new, float s1_spr_new, float x0_off_new, float y0_off_new, float pen_new_up, float pen_new_dn)
{
  if (arm0_mm_new != NOVALUE)
    arm0_mm = arm0_mm_new;
  if (arm1_mm_new != NOVALUE)
    arm1_mm = arm1_mm_new;
  if (s0_spr_new != NOVALUE)
    s0.update_config(s0_spr_new);
  if (s1_spr_new != NOVALUE)
    s1.update_config(s1_spr_new);
  if (x0_off_new != NOVALUE)
    x0_offset_mm = x0_off_new;
  if (y0_off_new != NOVALUE)
    y0_offset_mm = y0_off_new;
  if (pen_new_up != NOVALUE)
    servo_up_pwm = pen_new_up;
  if (pen_new_dn != NOVALUE)
    servo_dn_pwm = pen_new_dn;
}

void scara_bot::set_def_speeds(float new_accel, float new_vel)
{
  if (new_accel != NOVALUE)
    def_accel = new_accel;
  if (new_vel != NOVALUE)
    def_vel = new_vel;
}

void scara_bot::enable_motors(bool x, bool y)
{
  if (!x and !y)
  {
    x = true;
    y = true;
  }

  if (x)
    s0.enable();

  if (y)
    s1.enable();
}

void scara_bot::disable_motors(bool x, bool y)
{
  if (!x and !y)
  {
    x = true;
    y = true;
  }

  if (x)
    s0.disable();

  if (y)
    s1.disable();
}

void scara_bot::zero(float x_target_mm, float y_target_mm)
{
  x_target_mm = x_target_mm == NOVALUE ? 0.0 : x_target_mm;
  y_target_mm = y_target_mm == NOVALUE ? 0.0 : y_target_mm;

  float t0, t1;
  ik_solve(x_target_mm, y_target_mm, t0, t1);
  s0.set_zero_rads(t0);
  s1.set_zero_rads(t1);
//  s0.set_zero_rads(PI);
//  s1.set_zero_rads(2*PI);
}

void scara_bot::move_motor_linear(float x_target_mm, float y_target_mm, float v_max)
{
  // Get start position
  float x_start, y_start;
  get_pos(x_start, y_start);

  // Populate with defaults if any are none
  v_max = v_max == NOVALUE ? def_vel : v_max / 60;
  float accel = def_accel;

  // If relative mode, do that
  if (absmode == false)
  {
    x_target_mm = x_target_mm == NOVALUE ? x_start : x_target_mm + x_start;
    y_target_mm = y_target_mm == NOVALUE ? y_start : y_target_mm + y_start;
  }
  else
  {
    x_target_mm = x_target_mm == NOVALUE ? x_start : x_target_mm;
    y_target_mm = y_target_mm == NOVALUE ? y_start : y_target_mm;
  }

  // Calculate some basic move statistics
  float move_dist_mm = sqrt(pow(x_target_mm - x_start, 2) + pow(y_target_mm - y_start, 2));
  float accel_dist_mm = pow(v_max, 2) / (2 * accel);

  if(move_dist_mm < (2 * accel_dist_mm))
  {
    accel_dist_mm = move_dist_mm / 2;
  }
  float inflect_t0_s = sqrt((2 * accel_dist_mm) / accel);
  float inflect_t1_s = inflect_t0_s + (move_dist_mm - (2 * accel_dist_mm)) / v_max;
  float move_time_s = inflect_t1_s + inflect_t0_s;

//  Serial.print(v_max);
//  Serial.print("\t");
//  Serial.print(accel);
//  Serial.print("\t");
//  Serial.print(move_dist_mm);
//  Serial.print("\t");
//  Serial.print(accel_dist_mm);
//  Serial.print("\t");
//  Serial.print(x_start);
//  Serial.print("\t");
//  Serial.println(y_start);


  // Calculate when to take steps on the fly like a -boss- skrub
  uint8_t motion_state = 0; // 0: accelerating, 1: plateau, 2: decelerating, 3: finalize
  uint32_t t_start = micros();
  uint32_t t_step;

  float linear_dist_mm, t_elapsed_s, move_percent, xtar_mm, ytar_mm;
  while(true)
  {
    t_step = micros();
    t_elapsed_s = t_step - t_start;
    t_elapsed_s /= 1000000;

    switch(motion_state)
    {
      case 0: {
        linear_dist_mm = (accel * pow(t_elapsed_s, 2)) / 2;
        if(t_elapsed_s > inflect_t0_s) motion_state++;
        break;
      }
      case 1: {
        linear_dist_mm = accel_dist_mm + v_max * (t_elapsed_s - inflect_t0_s);
        if(t_elapsed_s > inflect_t1_s) motion_state++;
        break;
      }
      case 2: {
        linear_dist_mm = move_dist_mm - ((accel * pow(move_time_s - t_elapsed_s, 2)) / 2);
        if(t_elapsed_s > move_time_s) motion_state++;
        break;
      }
      case 3: {
        linear_dist_mm = move_dist_mm;
        break;
      }
    }
    move_percent = linear_dist_mm / move_dist_mm;
    xtar_mm = x_start + move_percent * (x_target_mm - x_start);
    ytar_mm = y_start + move_percent * (y_target_mm - y_start);

    float t0, t1;
    ik_solve(xtar_mm, ytar_mm, t0, t1);
    s0.set_rad_target(t0);
    s1.set_rad_target(t1);

    bool stepped = false;
    stepped = s0.step_if_needed() ? true : stepped;
    stepped = s1.step_if_needed() ? true : stepped;

//    debug_print();

    if(motion_state == 3 && !stepped) break;
  }
}

void scara_bot::move_motor_arc(float x_target_mm, float y_target_mm, float ival, float jval, float v_max, bool cw)
{
  // Ugh math sucks
}

double scara_bot::cos_solve(float l1, float l2, float l3)
{
  double output = -pow(l1, 2) + pow(l2, 2) + pow(l3, 2);
  output /= (2 * l2 * l3);
  return acos(output);
}

void scara_bot::ik_solve(float xtar_mm, float ytar_mm, float &theta0, float &theta1)
{
  float x_shifted = xtar_mm - x0_offset_mm;
  float y_shifted = ytar_mm - y0_offset_mm;

  float q2 = acos((pow(x_shifted, 2) + pow(y_shifted, 2) - pow(arm0_mm, 2) - pow(arm1_mm, 2)) / (2 * arm0_mm * arm1_mm));
  float q1 = atan2(y_shifted, x_shifted) + PI - atan((arm1_mm* sin(q2)) / (arm0_mm + arm1_mm*cos(q2)));

  theta0 = PI - q1;
  theta1 = (PI - q1) + (PI - q2);
  s0.set_rad_target(PI - q1);
  s1.set_rad_target((PI - q1) + (PI - q2));
}

void scara_bot::set_pos_mode(bool abs_true)
{
  absmode = abs_true;
}

void scara_bot::debug_print()
{
  Serial.print(s0.get_rads());
  Serial.print('\t');
  Serial.println(s1.get_rads());
}

void scara_bot::get_pos(float &xpos_mm, float &ypos_mm)
{
  float theta0 = s0.get_rads();
  float theta1 = s1.get_rads() - theta0;

  // Calculate line from scara origin to end effector
  float len_a = sqrt(pow(arm0_mm, 2) + pow(arm1_mm, 2) - 2 * arm0_mm * arm1_mm * cos(theta1));
  float angle_a = theta0 - cos_solve(arm1_mm, arm0_mm, len_a);

  // Get effector relative position
  xpos_mm = len_a * cos(angle_a);
  ypos_mm = -len_a * sin(angle_a);

  // Apply zero offset
  xpos_mm = xpos_mm + x0_offset_mm;
  ypos_mm = y0_offset_mm + ypos_mm;
}

void scara_bot::lower_pen()
{
  p_servo.write(servo_dn_pwm);
  delay(3 * fabs(servo_up_pwm - servo_dn_pwm));
}

void scara_bot::raise_pen()
{
  p_servo.write(servo_up_pwm);
  delay(3 * fabs(servo_up_pwm - servo_dn_pwm));
}


/* GCODE PARSER STUFF */

gcode_command_floats::gcode_command_floats(vector<string> inputs)
{
  if (inputs.size() == 1)
    return;

  for(uint16_t arg_i = 1; arg_i < inputs.size(); arg_i++)
  {
    char char_value = '\0';
    float float_value = NOVALUE;
    parse_float(inputs[arg_i], char_value, float_value);

    commands.push_back(tolower(char_value));
    values.push_back(float_value);
  }
}

float gcode_command_floats::fetch(char com_key)
{
  vector<char>::iterator itr = find(commands.begin(), commands.end(), com_key);
  if (itr != commands.cend())
  {
    return values[distance(commands.begin(), itr)];
  }

  return NOVALUE;
}

bool gcode_command_floats::com_exists(char com_key)
{
  vector<char>::iterator itr = find(commands.begin(), commands.end(), com_key);
  if (itr != commands.cend())
  {
    return true;
  }

  return false;
}

void gcode_command_floats::parse_float(string inpt, char &cmd, float &value)
{
  if (inpt.length() > 0)
  {
    cmd = inpt[0];
    if (inpt.length() == 1)
      return;

    string temp_arg_char = "";
    for (uint32_t i = 1; i < inpt.length(); i++)
    {
      temp_arg_char += inpt[i];
    }
  
    value = stof(temp_arg_char);
  }
}
