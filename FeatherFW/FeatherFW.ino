#include "tacbot.h"
#include "funks.h"

#define Serial SERIAL_PORT_USBVIRTUAL

void setup()
{
  Serial.begin(250000);
  pixel.begin();
}

void loop()
{
  // Initialize some stuff
  setLEDColor(200, 0, 0);
  unsigned long startTime_us = micros();
  unsigned long t_elapsed_us;
  stepper s0, s1;
  Servo pen_servo;
  s0.init(s0_step, s0_dir, s0_en, false);
  s1.init(s1_step, s1_dir, s1_en, false);

  scara_bot bot;
  bot.init(s0, s1, pen_servo);

  char serial_data[MAX_MSG_LEN];
  setLEDColor(100, 0, 0);

  // Init vars
  char base_cmd, char_value;
  int32_t base_value, int_value;
  float float_value;

  // Start main response loop
  while (true)
  {
    t_elapsed_us = micros() - startTime_us;
    clear_data(serial_data);
    if (respondToSerial(serial_data)) 
    {
      setLEDColor(100, 50, 0);

      // Parse input into data chunks
      vector<string> args;
      parse_inputs(serial_data, args);
      parse_int(args[0], base_cmd, base_value);

      switch (tolower(base_cmd)) 
      {
        case 'g': {
          switch (base_value) 
          {
            case 0:
            case 1: {
              // LINEAR MOVE
              float xpos, ypos, feedrate;
              gcode_command_floats gcode(args);
              bot.move_motor_linear(gcode.fetch('x'), gcode.fetch('y'), gcode.fetch('f'));
              break;
            }
            case 2: {
              // ARC MOVE CW
              gcode_command_floats gcode(args);
              bot.move_motor_arc(gcode.fetch('x'), gcode.fetch('y'), gcode.fetch('i'), gcode.fetch('j'), gcode.fetch('f'), true);
              break;
            }
            case 3: {
              // ARC MOVE CCW
              gcode_command_floats gcode(args);
              bot.move_motor_arc(gcode.fetch('x'), gcode.fetch('y'), gcode.fetch('i'), gcode.fetch('j'), gcode.fetch('f'), false);
              break;
            }
            case 28: {
              Serial.println("TODO homing");
              break;
            }
            case 90: {
              // Absolute positioning
              bot.set_pos_mode(true);
              break;
            }
            case 91: {
              // Relative positioning
              bot.set_pos_mode(false);
              break;
            }
            case 92: {
              // This is implemented wrong currently but idc deal with it
              gcode_command_floats gcode(args);
              bot.zero(gcode.fetch('x'), gcode.fetch('y'));
              break;
            }
          }
          break;
        }
      case 'm': {
          switch (base_value) 
          {
            case 17: {
              // Enable Steppers
              gcode_command_floats gcode(args);
              bot.enable_motors(gcode.com_exists('x'), gcode.com_exists('y'));
              break;
            }
            case 84: {
              // Disable Steppers
              gcode_command_floats gcode(args);
              bot.disable_motors(gcode.com_exists('x'), gcode.com_exists('y'));
              break;
            }
            case 201: {
              // Set Acceleration Limits
              gcode_command_floats gcode(args);
              bot.set_def_speeds(gcode.com_exists('a'), gcode.com_exists('v'));
              break;
            }
          }
          break;
        }
      case 'c': {
          switch (base_value) 
          {
            case 0: {
              // configure hardware stuff
              gcode_command_floats gcode(args);
              bot.configure(gcode.fetch('a'), gcode.fetch('b'), gcode.fetch('c'), gcode.fetch('d'), gcode.fetch('e'), gcode.fetch('f'));
              break;
            }
            case 1: {
              // Set Zero Offset
              Serial.println("TODO Set Zero Offset");
              break;
            }
          }
        }
        break;
      }
      Serial.println("ok");
      setLEDColor(0, 100, 0);
    }
  }
}
