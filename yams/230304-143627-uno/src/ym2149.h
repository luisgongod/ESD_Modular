#include <Arduino.h>
// MSB (PB3) is connected to BDIR
// LSB (PB2) is connected to BC1
// +5V is connected to BC2
#define DATA_READ (0x01 << 2)
#define DATA_WRITE (0x02 << 2)
#define ADDRESS_MODE (0x03 << 2)


#define CLK_PIN 11                                  // OC2A pin - cannot be changed
#define CLK_ARDUINO_FREQ 16000000                    // Arduino clock frequency
#define PRESCALE_FACTOR 1                           // required in order to get reasonable accuracy
#define YM_CLK 1000000                             // 1MHz clock


// Sets a 4MHz clock OC2A (PORTB3)
void set_ym_clock(void) {
  

  TCCR2B = B00000001;                               // set CS20, clear CS21, CS22 and WGM22
  TCCR2A = B01000010;                               // set COM2A0 and WGM21, clear COM2A1 and WGM20

// calculate and load the timer data timer 
  OCR2A  = ((float)CLK_ARDUINO_FREQ / (YM_CLK * 2 * PRESCALE_FACTOR)) -1;  

// Set up the output pin
  pinMode(CLK_PIN, OUTPUT);                          // turn on output pin   


}

void set_bus_ctl(void) {
  DDRC |= 0x0c; // Bits 2 and 3
}

void set_data_out(void) {
  DDRC |= 0x03; // Bits 0 and 1
  DDRD |= 0xfc; // Bits 2 to 7
}

void set_data_in(void) {
  DDRC &= ~0x03; // Bits 0 and 1
  DDRD &= ~0xfc; // Bits 2 to 7
}

void set_address(char addr) {
  set_data_out();
  PORTC = (PORTC & 0xf3) | ADDRESS_MODE;
  PORTC = (PORTC & 0xfc) | (addr & 0x03); // 2 first bits ont PORTC
  PORTD = (PORTD & 0x02) | (addr & 0xfc); // 6 last bits on PORTD
  _delay_us(1.); //tAS = 300ns
  PORTC = (PORTC & 0xf3) /*INACTIVE*/ ;
  _delay_us(1.); //tAH = 80ns
}

void set_data(char data) {
  set_data_out();
  PORTC = (PORTC & 0xfc) | (data & 0x03); // 2 first bits ont PORTC
  PORTD = (PORTD & 0x02) | (data & 0xfc); // 6 last bits on PORTD
  PORTC = (PORTC & 0xf3) | DATA_WRITE;
  _delay_us(1.); // 300ns < tDW < 10us
  PORTC = (PORTC & 0xf3) /*INACTIVE*/ ; // To fit tDW max
  _delay_us(1.); // tDH = 80ns
}

char get_data(void) {
  char data;
  set_data_in();
  PORTC = (PORTC & 0xf3) | DATA_READ;
  _delay_us(1.); // tDA = 400ns
  data = (PIND & 0xfc) | (PINB & 0x03);
  PORTC = (PORTC & 0xf3) /*INACTIVE*/ ;
  _delay_us(1.); // tTS = 100ns
  return data;
}

void send_data(char addr, char data) {
  set_address(addr);
  set_data(data);
}

char read_data(char addr) {
  set_address(addr);
  return get_data();
}
