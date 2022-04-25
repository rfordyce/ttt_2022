#include <Servo.h>  // may need to install

// PIN values from Adeept docs and examples
//   http://www.adeept.com/learn/details/id/31

const int PIN_SERVO_BASE    = 9;
const int PIN_SERVO_JOINT_1 = 6;
const int PIN_SERVO_JOINT_2 = 5;

Servo s_base;
Servo s_joint1;
Servo s_joint2;

void setup() {
    // begin serial connection
    Serial.begin(9600);
    Serial.write("beginning\n");

    Serial.write("setting up Servos\n");
    // set up Servos
    pinMode(PIN_SERVO_BASE, OUTPUT);
    pinMode(PIN_SERVO_JOINT_1, OUTPUT);
    pinMode(PIN_SERVO_JOINT_2, OUTPUT);
    // zero out servos and then attach to them
    // TODO get these from EEPROM to avoid any extra boot twitch
    //   https://forum.arduino.cc/t/easiest-way-to-avoid-servo-twitch-on-power-up/187028/15
    s_base.write(90);
    s_joint1.write(90);
    s_joint2.write(90);
    s_base.attach(PIN_SERVO_BASE);
    s_joint1.attach(PIN_SERVO_JOINT_1);
    s_joint2.attach(PIN_SERVO_JOINT_2);

    Serial.write("ready to take commands\n");
}

void loop()
{
    delay(2000);
    s_base.write(20);
    Serial.write("long delay loop\n");
    delay(100000);  // ms?
}
