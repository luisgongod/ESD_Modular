#include <Arduino.h>
// MSB (PB3) is connected to BDIR
// LSB (PB2) is connected to BC1
// +5V is connected to BC2
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
  // PORTC = (PORTC & 0xf3) /*INACTIVE*/ ;
}

void set_data_port(char data) {
  PORTC = (PORTC & 0xfc) | (data & 0x03); // 2 first bits ont PORTC
  PORTD = (PORTD & 0x02) | (data & 0xfc); // 6 last bits on PORTD
}



void set_address(char addr) {
 

  ctl_set_address();
  set_data_port(addr);
  _delay_us(1.); //tAS = 300ns
  ctl_set_inactive();
  _delay_us(1.); //tAH = 80ns
}

void set_data(char data) {
 
  set_data_port(data);
    
  ctl_set_data();
  _delay_us(1.); // 300ns < tDW < 10us  
  ctl_set_inactive();
  _delay_us(1.); // tDH = 80ns
}


void send_data(char addr, char data) {
  set_address(addr);
  set_data(data);
}

void ym_init(void) {
  
  // DDRB = DDRB | B00111111; // All outputs except xtals
  // DDRC = DDRC | B00001011; // All outputs except analog input and I2C
  // DDRD = DDRD | B11110000; // All outputs except Rx, Tx, Interrupts

  // DDRC |= 0b00001100; // Bits 2 and 3 (BC1 and BDIR)
  DDRB |= 0b00000011; // Bits 0 and 1 (BC1 and BDIR)
  
  DDRC |= 0b00000011; // Bits 0 and 1 (data)
  DDRD |= 0b11111100; // Bits 2 to 7  (data)




  set_ym_clock();

  unsigned int i;
  // reset registers
  for (i=0; i<16; i++) {
    send_data(i, 0);
  }

}
