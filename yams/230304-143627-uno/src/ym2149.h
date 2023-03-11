#include <Arduino.h>

// +5V is connected to BC2 and RES 
#define DATA_READ (0x01)
#define DATA_WRITE (0x02)
#define ADDRESS_MODE (0x03)

#define CLK_PIN 11                                  // OC2A pin - cannot be changed
#define CLK_ARDUINO_FREQ 16000000                    // Arduino clock frequency
#define PRESCALE_FACTOR 1                           // required in order to get reasonable accuracy
#define YM_CLK 1000000                             // 1MHz clock

// Sets a 4MHz clock OC2A (PORTB3)
void set_ym_clock(void) {
  TCCR2B = B00000001;                               // set CS20, clear CS21, CS22 and WGM22
  TCCR2A = B01000010;                               // set COM2A0 and WGM21, clear COM2A1 and WGM20
  OCR2A  = ((float)CLK_ARDUINO_FREQ / (YM_CLK * 2 * PRESCALE_FACTOR)) -1;  
  pinMode(CLK_PIN, OUTPUT);                          // turn on output pin   
}


void ctl_set_address(void) {
  PORTB = (PORTB & 0b11111100) | ADDRESS_MODE;
}
void ctl_set_data(void) {
  PORTB = (PORTB & 0b11111100) | DATA_WRITE;
}
void ctl_set_inactive(void) {
  PORTB = (PORTB & 0b11111100) /*INACTIVE*/ ;
}

void set_data_at_port(char data) {
  PORTC = (PORTC & 0b11111100) | (data & 0b00000011); // 2 first bits ont PORTC    
  PORTB = (PORTB & 0b11001111) | ((data & 0b00001100)<<2); // next 2 bits on PORTD
  PORTD = (PORTD & 0b00001111) | (data & 0b11110000); // 4 last bits on PORTD Original PORTD & 0b00001110, idk why
}


void set_address(char addr) {
 
  ctl_set_address();
  set_data_at_port(addr);
  _delay_us(1.); //tAS = 300ns
  ctl_set_inactive();
  _delay_us(1.); //tAH = 80ns
}

void set_data(char data) {
 
  set_data_at_port(data);
    
  ctl_set_data();
  _delay_us(1.); // 300ns < tDW < 10us  
  ctl_set_inactive();
  _delay_us(1.); // tDH = 80ns
}


void send_data(char addr, char data) {
  set_address(addr);
  set_data(data);
}

void set_channel(char channel, char volume, uint16_t tone, bool envelope) {
  //switch case channel
  switch (channel)
  {
  case 0:
    send_data(0, tone & 0xFF);
    send_data(1, (tone >> 8) & 0xFF);
    send_data(8, (envelope << 4) | volume);
  
  case 1:
    send_data(2, tone & 0xFF);
    send_data(3, (tone >> 8) & 0xFF);
    send_data(9, (envelope << 4) | volume);

  case 2:
    send_data(4, tone & 0xFF);
    send_data(5, (tone >> 8) & 0xFF);
    send_data(10, (envelope << 4) | volume);

    break;
  
  default:
    break;
  }
  
}


void ym_init(void) {
  
  DDRB |= 0b00000011; // Bits 0 and 1 (BC1 and BDIR)  
  DDRC |= 0b00000011; // Bits 0 and 1 (data)
  DDRB |= 0b00110000; // Bits 2 and 3 (data)
  DDRD |= 0b11110000; // Bits 4 to 7  (data)

  set_ym_clock();

  unsigned int i;
  // reset registers
  for (i=0; i<16; i++) {
    send_data(i, 0);
  }

}
