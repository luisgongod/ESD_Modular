#include <Arduino.h>
#include <Adafruit_MCP23X17.h>
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

Adafruit_MCP23X17 mcp;

int analog_input[4];

void setup() 
{
  //Serial.begin(9600);
//  Serial.println(result);

  ym_init();

  if (!mcp.begin_I2C()) {
    // Serial.println("Error.");
    while (1);
  }

  mcp.pinMode(0, OUTPUT);
  mcp.pinMode(1, OUTPUT);
  mcp.pinMode(2, OUTPUT);
  mcp.pinMode(3, OUTPUT);

  send_data(7, 0xf8); // Only output clear sound
  send_data(8, 0x1f); // Volume of envelope Channel A
  send_data(9, 0x1f);// Volume of envelope Channel B
  send_data(0xa, 0x1f);// Volume of envelope Channel C
  send_data(11, 0x82); //freq of envelope fine
  send_data(12, 0x00); //freq of envelope coarse
  send_data(13, 0b00001010); //shape of envelope

}
void loop() {

for(int i=0; i<=3;i++){
    mcp.digitalWrite(i, HIGH);
    _delay_ms(5.);

    analog_input[i] = analogRead(A2);    
    mcp.digitalWrite(i, LOW);
    _delay_ms(10.);  
    
  }
int note = map(analog_input[0], 0, 1023, 0, 6);
int env_shape = map(analog_input[1], 0, 1023, 0, 15);
int env_freq = map(analog_input[2], 0, 1023, 0, 0xfff);
int decay_time = map(analog_input[3], 0, 1023, 0, 800);


      send_data(0, data[note] & 0xff);
      send_data(1, data[note] >> 8);
      send_data(2, data[note] >> 1 & 0xff);
      send_data(3, data[note] >> 9);
      send_data(4, data[note] >> 2 & 0xff);
      send_data(5, data[note] >> 10);
      send_data(11, env_freq & 0xff); //freq of envelope fine
      send_data(12, env_freq >> 8); //freq of envelope coarse
      send_data(13, env_shape); //shape of envelope
      send_data(7, 0xf8); //mixer on all
      delay(decay_time);
      

      send_data(7, 0xff); //mixer off all
      delay(decay_time/2);




  


    
  }
