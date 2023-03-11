#include <Arduino.h>
#include "ym2149.h"
//modified to work with arduino ide
// Notes
// Np = 2e6 / (16 * Fn)
#define C 239
#define D 213
#define E 190
#define F 179
#define G 159
#define A 142
#define B 127


unsigned int i;
unsigned int data[7] = {C, D, E, F, G, A, B};

void setup() 
{
  //Serial.begin(9600);
//  Serial.println(result);

  
  pinMode(10, OUTPUT);

  ym_init();

  

  // reset registers
  for (i=0; i<16; i++) {
    send_data(i, 0);
  }

  send_data(7, 0xf8); // Only output clear sound
  send_data(8, 0x0f);
  send_data(9, 0x0f);
  send_data(10, 0x0f);
  send_data(11, 0x0f); //freq of envelope fine
  send_data(12, 0x0f); //freq of envelope coarse
  send_data(13, 0x08); //shape of envelope

}
void loop() {

  //blink led
  digitalWrite(10, HIGH);
  delay(300);
  digitalWrite(10, LOW);
  delay(300);


      // int analogValue = analogRead(A4);
      // //map the analog value to a 16 option range
      // int i = map(analogValue, 0, 1023, 0, 6);


      // send_data(0, data[i] & 0xff);
      // send_data(1, data[i] >> 8);
      // send_data(2, data[i] >> 1 & 0xff);
      // send_data(3, data[i] >> 9);
      // send_data(4, data[i] >> 2 & 0xff);
      // send_data(5, data[i] >> 10);
      // send_data(7, 0xf8); //mixer on all
      // _delay_ms(200.);

      // send_data(7, 0xff); //mixer off all
      // _delay_ms(300.);

    
  }
