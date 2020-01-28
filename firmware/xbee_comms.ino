#include <Printers.h>
#include <XBee.h>

#include <LiquidCrystal.h>

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
uint8_t option = 0;
uint8_t payload[] = {0,0,0,0};
Rx16Response rx16 = Rx16Response();
uint16_t addr_Central_Station= 0xFFFF;
Tx16Request tx = Tx16Request(addr_Central_Station, payload, sizeof(payload));


void setup() {
  Serial.begin(115200);
  xbee.setSerial(Serial);
  pinMode(8,OUTPUT);

}

void loop() {
     xbee.readPacket();
    if (xbee.getResponse().isAvailable()) {
      
      if (xbee.getResponse().getApiId() == RX_16_RESPONSE || xbee.getResponse().getApiId() == RX_64_RESPONSE) {
        
        if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
                xbee.getResponse().getRx16Response(rx16);
                option = rx16.getOption();
                int s;
                s = (rx16.getData(0)-48);
                if(s==1)
                digitalWrite(8,HIGH);
                delay(1000);
                payload[0]='D' & 0xff;
                payload[1]='O' & 0xff;
                payload[2]='N' & 0xff;
                payload[3]='E' & 0xff;
                xbee.send(tx);
                }
      }
    }
    digitalWrite(8,LOW);
}
