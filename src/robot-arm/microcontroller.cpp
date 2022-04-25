#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include <Servo.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);
sensors_event_t event;
uint8_t bno_calibration_data = 0;  // fill to avoid calibration

// PIN values from Adeept docs and examples
//   http://www.adeept.com/learn/details/id/31

const int PIN_SERVO_BASE    = 9;
const int PIN_SERVO_JOINT_1 = 6;
const int PIN_SERVO_JOINT_2 = 5;

Servo s_base;
Servo s_joint1;
Servo s_joint2;

char buffer[128];   // FIXME for unsafe sprintf use .. but that's probably enough


void calibrate_bno() {
    if (bno_calibration_data != 0) {  // set by user
        bno.setSensorOffsets(&bno_calibration_data);
        return 0;
    }

    // attempt calibration in a loop
    Serial.write("attempting calibration\n");
    while (!bno.isFullyCalibrated()) { // TODO ranges from 0-3 .. is less than 3 sufficient?
        // TODO perform calibration by moving servos
    }
    // does it make sense to write to EEPROM or is it better to let the user update bno_calibration_data?
    Serial.write("calibrated\n");
    Serial.write(bno_calibration_data);  // FIXME special formatting so user can read to write into block
}

void arm_to_neutral() {
    s_base.write(180);
    s_joint1.write(90);
    s_joint2.write(180);
    delay(500);
}


void draw2d(
    int16_t angle_base_start,
    int16_t angle_base_end,
    int16_t angle_joint1_start,
    int16_t angle_joint1_end,
    int16_t angle_joint2_start,
    int16_t angle_joint2_end,
    double count = 20  // do degrees have enough resolution?
) {
    /* draw on paper surface between the two points
       calculates a series of <count> points between the two servo positions
    */

    // NOTE be careful of joint move ordering
    //   I somewhat suspect it's best to always move joint1 last
    //   (base, j1, j2)
    // generally want to avoid letting the arm drag on the paper

    // FIXME these shouldn't be magic
    if (s_joint2.read() < 120)  // BEWARE this is cached .write(), true .read() is impossible without encoder
        s_joint2.write(angle_joint2_start - 10);  // FIXME is this dangerous to always do? may crash into camera
    delay(500);


    // TODO is a meshgrid better? (really want 3d linspace?)
    //   consider https://github.com/xiaohongchen1991/meshgen (MIT)
    // calculate deltas
    double djb = (double)(angle_base_end   - angle_base_start)   / (double)count;  // NOTE these can be negative
    double dj1 = (double)(angle_joint1_end - angle_joint1_start) / (double)count;
    double dj2 = (double)(angle_joint2_end - angle_joint2_start) / (double)count;
    // move each servo to the Nth point along the way
    Serial.print("djb:"); Serial.print(djb);  // XXX just debug deltas
    Serial.print("|dj1:"); Serial.print(dj1);
    Serial.print("|dj2:"); Serial.print(dj2);
    Serial.print("\n");
    for (double i = 0; i < count; i++) {
        s_base.write(angle_base_start     + (int8_t)(i * djb));  // NOTE these must be signed!
        s_joint1.write(angle_joint1_start + (int8_t)(i * dj1));
        s_joint2.write(angle_joint2_start + (int8_t)(i * dj2));
        delay(500);  // TODO is this long enough?
    }

    // raise the arm a little
    //   yuck.. is it worth making my own crash avoidance?
    //   G-code-like -> compute solids -> plan route
    //   I suspect it's overkill, especially without the 9-DOF
    Serial.print("raising arm 10deg to detach pen from paper\n");
    s_joint2.write(angle_joint2_start - 10);
    delay(500);
}


void draw_X(uint8_t draw_index) { // 1-9
    // just let the arm do Xs for now to avoid drawing O
    /*
        positions
        1 2 3
        4 5 6
        7 8 9
    */
    // FIXME about this implementation, which is quite poor
    // bespoke point selection implementation without 9-DOF working
    // plausibly this would work well if I had encoders, but there is a great amount of slop
    // even more painful work to do for each side of the X
    //   this is probably much easier to just calculate a collection of points in Python
    //   sympy(arm component measurements) -> np.linspace -> cpp vector
    switch(draw_index) {
        // case 1: draw2d(100, 90, 4, 27, 100, 110); break; // eyeball'd
        // case 1: draw2d(100, 90, 10, 20, 100, 110); break; // eyeball'd
        // case 1: draw2d(100, 90, 10, 15, 100, 110); break;  // eyeball'd
        case 1: draw2d(100, 90, 15, 15, 100, 120); break;  // eyeball'd
        default:
            Serial.write("default case\n");
    }
}



void setup() {
    // begin serial connection
    Serial.begin(9600);
    Serial.write("beginning\n");

    /* Initialise the sensor */
    if(!bno.begin()) {
        Serial.write("couldn't detect BNO055 wiring and i2c address\n");
        while(1);
    }
    Serial.write("BNO055 initialised \n");
    // delay(1000);  // from BNO055 Adafruit examples .. does this actually do anything?
    bno.setExtCrystalUse(true);

    // set up Servos
    Serial.write("setting up Servos\n");
    pinMode(PIN_SERVO_BASE, OUTPUT);
    pinMode(PIN_SERVO_JOINT_1, OUTPUT);
    pinMode(PIN_SERVO_JOINT_2, OUTPUT);
    // zero out servos and then attach to them
    // TODO get these from EEPROM to avoid any extra boot twitch
    //   https://forum.arduino.cc/t/easiest-way-to-avoid-servo-twitch-on-power-up/187028/15

    // face left (avoids hitting camera)
    arm_to_neutral();
    s_base.attach(PIN_SERVO_BASE);
    s_joint1.attach(PIN_SERVO_JOINT_1);
    s_joint2.attach(PIN_SERVO_JOINT_2);

    // calibrate_bno();  // FIXME does nothing yet
    // reset bno to zero here to have some guess at where it is
    // face left again in preparation

    // displaybno();  // FIXME does nothing yet
    arm_to_neutral();
    // now face foward in same orientation
    delay(1000);
    s_base.write(90);

    Serial.write("ready to take commands\n");
}

void loop()
{
    delay(1000);

    // XXX
    draw_X(1);
    Serial.write("success, entering dead loop");
    arm_to_neutral();
    while(1);
}
