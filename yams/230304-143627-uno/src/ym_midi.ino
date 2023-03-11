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

  
  // pinMode(10, OUTPUT);

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
  

    // PORTC = (PORTC & 0b11111100) | (0x1 & 0b00000011);
    // _delay_ms(400.);
    // PORTC = (PORTC & 0b11111100) | (0x2 & 0b00000011);
    // _delay_ms(400.);
  
    // PORTB = (PORTB & 0b11111100) | ADDRESS_MODE; 
    // _delay_ms(400.);
    //   PORTB = (PORTB & 0b11111100); //INACTIVE
    // _delay_ms(400.);


  
  // PORTB = (PORTB & 0b11111100) | ADDRESS_MODE; //Set BC1 and BDIR to address mode
  // _delay_ms(500.);
  // PORTB = (PORTB & 0b11111100) | DATA_INACTIVE; //Set BC1 and BDIR to address mode
  // _delay_ms(500.);
  // PORTB = (PORTB & 0b11111100) | DATA_WRITE; //Set BC1 and BDIR to address mode
  // _delay_ms(500.);
  // PORTB = (PORTB & 0b11111100) | DATA_READ; //Set BC1 and BDIR to address mode
  // _delay_ms(500.);

  // set_data_out();

  
  // PORTB = (PORTB & 0b11111100) | ADDRESS_MODE; //Set BC1 and BDIR to address mode

  // PORTC = (PORTC & 0b11111100) | (1 & 0b00000011); // 0,1 address bits on PORTC
  // PORTB = (PORTB & 0b11001111) | (1<<2 & 0b00110000); // 2,3 address bits on PORTB

  // _delay_ms(500.); //tAS = 300ns
  // PORTB = (PORTB & 0b11111100) | DATA_INACTIVE ; //INACTIVE
  
  // _delay_ms(1000.); //tAH = 80ns


  // PORTB = (PORTB & 0b11111100) | ADDRESS_MODE; //Set BC1 and BDIR to address mode
  // PORTC = (PORTC & 0b11111100) | (2 & 0b00000011); // 0,1 address bits on PORTC
  // PORTB = (PORTB & 0b11001111) | (2<<2 & 0b00110000); // 2,3 address bits on PORTB
  // _delay_ms(500.); //tAS = 300ns
  // PORTB = (PORTB & 0b11111100) | DATA_INACTIVE ; //INACTIVE  
  // _delay_ms(1000.); //tAH = 80ns




  for(i=0; i<4; i++){
    
      digitalWrite(10, HIGH);
  
      send_data(0, data[i] & 0xff);
      send_data(1, data[i] >> 8);
      send_data(2, data[i] >> 1 & 0xff);
      send_data(3, data[i] >> 9);
      send_data(4, data[i] >> 2 & 0xff);
      send_data(5, data[i] >> 10);
      send_data(7, 0xf8); //mixer on all
      _delay_ms(200.);

      send_data(7, 0xff); //mixer off all
      digitalWrite(10, LOW);
      _delay_ms(300.);
  }

      // int analogValue = analogRead(A4);
      // //map the analog value to a 16 option range
      // int i = map(analogValue, 0, 1023, 0, 6);



    
  }
