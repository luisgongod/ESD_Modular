#include <Arduino.h>
// MSB (PB3) is connected to BDIR
// LSB (PB2) is connected to BC1
// +5V is connected to BC2
#define DATA_READ 0x01
#define DATA_WRITE 0x02
#define ADDRESS_MODE 0x03


#define CLK_PIN 11                                  // OC2A pin - cannot be changed
#define CLK_ARDUINO_FREQ 16000000                    // Arduino clock frequency
#define PRESCALE_FACTOR 1                           // required in order to get reasonable accuracy
#define YM_CLK 1000000                             // 1MHz clock


// Notes frequency in program memory from C0 to B7
// const uint16_t PROGMEM NoteFreq[] = {
// 3823,3609,3406,3213,3034,2863,2703,2551,2408,2273,2145,2025,1911,1804,1703,1607,1517,1432,1351,1276,1204,1136,1073,1012,956,902,851,804,758,716,676,638,602,568,536,506,478,451,426,402,379,358,338,319,301,284,268,253,239,225,213,201,190,179,169,159,150,142,134,127,119,113,106,100,95,89,84,80,75,71,67,63,60,56,53,50,47,45,42,40,38,36,34,32,30,28,27,25,24,22,21,20,19,18,17,16
// };


// Sets a 4MHz clock OC2A (PORTB3)
void set_ym_clock(void) {  

  TCCR2B = B00000001;                               // set CS20, clear CS21, CS22 and WGM22
  TCCR2A = B01000010;                               // set COM2A0 and WGM21, clear COM2A1 and WGM20

  OCR2A  = ((float)CLK_ARDUINO_FREQ / (YM_CLK * 2 * PRESCALE_FACTOR)) -1;  
  pinMode(CLK_PIN, OUTPUT); 

}

// void set_bus_ctl(void) {
//   DDRC |= 0x0c; // Bits 2 and 3
// }

// void set_data_out(void) {
 
// }

// void set_data_in(void) {
//   DDRC &= ~0x03; // Bits 0 and 1
//   DDRD &= ~0xfc; // Bits 2 to 7
// }

void set_address(char addr) {
  // set_data_out();

  PORTB = (PORTB & 0b11111100) | ADDRESS_MODE; //Set BC1 and BDIR to address mode

  // PORTC = (PORTC & 0xf3) | ADDRESS_MODE;





  // PORTC = (PORTC & 0xfc) | (addr & 0x03); // 0,1 address bits on PORTC
  PORTC = (PORTC & 0b11111100) | (addr & 0b00000011); // 0,1 address bits on PORTC

  // PORTD = (PORTD & 0x02) | (addr & 0xfc); // 6 last bits on PORTD
  PORTB = (PORTB & 0b11001111) | (addr<<2 & 0b00110000); // 2,3 address bits on PORTB


  _delay_us(1.); //tAS = 300ns
  PORTB = (PORTB & 0b11111100); //INACTIVE
  // PORTC = (PORTC & 0xf3) /*INACTIVE*/ ;
  _delay_us(1.); //tAH = 80ns
}

void set_data(char data) {
  // set_data_out();
  // PORTC = (PORTC & 0xfc) | (data & 0x03); // 2 first bits ont PORTC
  // PORTD = (PORTD & 0x02) | (data & 0xfc); // 6 last bits on PORTD
  
  // PORTC = (PORTC & 0xf3) | DATA_WRITE;
  // _delay_us(1.); // 300ns < tDW < 10us
  // PORTC = (PORTC & 0xf3) /*INACTIVE*/ ; // To fit tDW max
  // _delay_us(1.); // tDH = 80ns

  PORTC = (PORTC & 0b11111100) | (data & 0b00000011); // 0,1 data bits on PORTC
  PORTB = (PORTB & 0b11001111) | (data<<2 & 0b00110000); // 2,3 data bits on PORTB
  PORTD = (PORTD & 0b00001111) | (data & 0b1111000); // 4,5,6,7 data bits on PORTD



  PORTB = (PORTB & 0b11111100) | DATA_WRITE; //Set BC1 and BDIR to data write mode
  _delay_us(1.); // 300ns < tDW < 10us
  PORTB = (PORTB & 0b11111100); //INACTIVE
  _delay_us(1.); // tDH = 80ns
}

// char get_data(void) {
//   char data;
//   set_data_in();
//   PORTC = (PORTC & 0xf3) | DATA_READ;
//   _delay_us(1.); // tDA = 400ns
//   data = (PIND & 0xfc) | (PINB & 0x03);
//   PORTC = (PORTC & 0xf3) /*INACTIVE*/ ;
//   _delay_us(1.); // tTS = 100ns
//   return data;
// }

void send_data(char addr, char data) {
  set_address(addr);
  set_data(data);
}

// char read_data(char addr) {
//   set_address(addr);
//   return get_data();
// }


void ym_init(void) {
  // Set data out


  /* Pin Port mapping
    Port B: 0 : Data Control BC1
            1 : Data Control BCDIR
            2 : Not used
            3 : YM Clock
            4 : YM Data bits 2
            5 : YM Data bits 3
            6,7 : Not used (xtal)
    
    Port C: 0 : YM Data bits 0
            1 : YM Data bits 1
            2 : Mux Analog input
            3 : Not used            
            4,5 : I2C
            6,7 : Only accessible in Arduino mini
    
    Port D: 0 : Rx
            1 : Tx
            2 : Interrupt 0
            3 : Interrupt 1
            4 : YM Data bit 4
            5 : YM Data bit 5
            6 : YM Data bit 6
            7 : YM Data bit 7
    */

  DDRB = DDRB | B00111111; // All outputs except xtals
  DDRC = DDRC | B00001011; // All outputs except analog input and I2C
  DDRD = DDRD | B11110000; // All outputs except Rx, Tx, Interrupts


  set_ym_clock();

  send_data(0x07, 0x3f); // Enable all channels
  send_data(0x08, 0x00); // Disable noise
  send_data(0x0e, 0x00); // Disable envelope
  send_data(0x0f, 0x00); // Disable envelope
}