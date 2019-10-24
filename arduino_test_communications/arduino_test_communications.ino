/*
  Test communications

  Waits for input from a Raspberry Pi (or any other serial device),
  sends a return message confirming receipt, and then turns an LED
  on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman
  modified 23 May 2019
  by Benjamin Jantzen

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Blink
*/

int params_set = 0;
int count = 0;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
}

// the loop function runs over and over again forever
void loop() {
  if(params_set ==0 && Serial.available()>0){
    //char msg = Serial.read();
    float msg = Serial.parseFloat();
    Serial.println(msg);
    params_set = 1;
  }
  else if(params_set == 1){
    // blink
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(100);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(100); // wait for a second
    if(Serial.availableForWrite() == 63){
      Serial.println(count);
    }
    count++;
  }
}
