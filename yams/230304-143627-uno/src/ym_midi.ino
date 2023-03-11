#include <Arduino.h>
#include "ym2149.h"
//modified to work with arduino ide
// Notes
// Np = 2e6 / (16 * Fn)
#define C (unsigned int)(2000000 / (16*130.81))
#define D (unsigned int)(2000000 / (16*146.83))
#define E (unsigned int)(2000000 / (16*164.81))
#define F (unsigned int)(2000000 / (16*174.61))
#define G (unsigned int)(2000000 / (16*196.00))
#define A (unsigned int)(2000000 / (16*220.00))
#define B (unsigned int)(2000000 / (16*246.94))


unsigned int i;
unsigned int data[7] = {C, D, E, F, G, A, B};

void setup() 
{
  //Serial.begin(9600);
//  Serial.println(result);


  ym_init();

  send_data(7, 0xf8); // Only output clear sound
  send_data(8, 0x0f); // Volume of envelope Channel A
  send_data(9, 0x0f);// Volume of envelope Channel B
  send_data(0xa, 0x0f);// Volume of envelope Channel C
  send_data(11, 0x82); //freq of envelope fine
  send_data(12, 0x00); //freq of envelope coarse
  send_data(13, 0b00001010); //shape of envelope

}
void loop() {


for(i=0; i<4; i++){
      send_data(0, data[i] & 0xff);
      send_data(1, data[i] >> 8);
      send_data(2, data[i] >> 1 & 0xff);
      send_data(3, data[i] >> 9);
      send_data(4, data[i] >> 2 & 0xff);
      send_data(5, data[i] >> 10);
      send_data(7, 0xf8); //mixer on all
      _delay_ms(200.);

      // send_data(7, 0xff); //mixer off all
      _delay_ms(300.);



}
  


    
  }
