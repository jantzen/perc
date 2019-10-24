/*!
 * @file mprls_simpletest.ino
 *
 * A basic test of the sensor with default settings
 * 
 * Designed specifically to work with the MPRLS sensor from Adafruit
 * ----> https://www.adafruit.com/products/3965
 *
 * These sensors use I2C to communicate, 2 pins (SCL+SDA) are required
 * to interface with the breakout.
 *
 * Adafruit invests time and resources providing this open source code,
 * please support Adafruit and open-source hardware by purchasing
 * products from Adafruit!
 *
 * Written by Limor Fried/Ladyada for Adafruit Industries.  
 *
 * MIT license, all text here must be included in any redistribution.
 *
 */
 
#include <Wire.h>
#include "Adafruit_MPRLS.h"

// You dont *need* a reset and EOC pin for most uses, so we set to -1 and don't connect
#define RESET_PIN  -1  // set to any GPIO pin # to hard-reset on begin()
#define EOC_PIN    -1  // set to any GPIO pin to read end-of-conversion by pin
Adafruit_MPRLS mpr = Adafruit_MPRLS(RESET_PIN, EOC_PIN);
int Relay = 2; //Digital pin D2
int pump = 0; //Start pump in off state
int ptol_set = 0; //indicate parameters not yet received
int pset_set = 0;
float pset = -1; // set initial nonsense value for pressure setpoin
float ptol = -1; // set nonsense value for error tolerance

void setup() {
  Serial.begin(115200);
  if (! mpr.begin()) {
    while (1) {
      delay(10);
    }
  }
  pinMode(Relay, OUTPUT); // declare pin Relay as output
  digitalWrite(Relay, LOW); // make sure the circuit is closed (pump off)
}

void loop() {
  if(pset_set == 0 && Serial.available() > 0){
    float tmp = Serial.parseFloat();
    if (1500 >= tmp && tmp >= 0){
      pset = tmp;
      Serial.println(1);
    }
    pset_set = 1;
  }
  else if(ptol_set == 0 && Serial.available() > 0){
    float tmp = Serial.parseFloat();
    if (100 >= tmp && tmp >= 1){
      ptol = tmp;
      Serial.println(1);
    }
    ptol_set = 1;
  }
  else if((pset != -1) && (ptol != -1)){
    float pressure_hPa = mpr.readPressure();
    if (Serial.availableForWrite() == 63){
      Serial.println(pressure_hPa);
    }
    if ((pressure_hPa < pset - ptol) && pump == 0) {
//      Serial.println("Switching pump ON.");
      digitalWrite(Relay, HIGH);
      pump = 1;
    }
    if ((pressure_hPa > pset + ptol) && pump == 1) {
//      Serial.println("Switching pump OFF.");
      digitalWrite(Relay, LOW);
      pump = 0;
    }
    char tmp = Serial.read();
    if(tmp == "r"){
      pset=-1;
      ptol=-1;
      pset_set=0;
      ptol_set=0;
    }
  }
  delay(100);
}
