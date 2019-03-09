#include <DCMotor.h>

#include <XBee.h>

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();

Rx16Response rx16 = Rx16Response();
#define BOTID 4

uint8_t option = 0;
uint8_t data;

dcm m1(8,22,23);
dcm m2(9,24,25);
dcm m3(10,26,27);
dcm d(11,28,29);

volatile long int oldtime1,c1=0,t1,rpm1,e1,eo1,es1,ed1,kp1=4,kd1=1,ki1=1,pid1,r1,dir1,rpmo1;
volatile long int oldtime2,c2=0,t2,rpm2,e2,eo2,es2,ed2,kp2=4,kd2=1,ki2=1,pid2,r2,dir2,rpmo2;
volatile long int oldtime3,c3=0,t3,rpm3,e3,eo3,es3,ed3,kp3=4,kd3=1,ki3=1,pid3,r3,dir3,rpmo3;

volatile int k,ds;

void setup() 
{
  m3.minit();
  m2.minit();
  m1.minit();
  d.minit();
  Serial.begin(115200);
  xbee.setSerial(Serial);
  pinMode(7,OUTPUT);
}

void loop() 
{
    xbee.readPacket();
    
    if (xbee.getResponse().isAvailable()) {
      
      if (xbee.getResponse().getApiId() == RX_16_RESPONSE || xbee.getResponse().getApiId() == RX_64_RESPONSE) {
        
        if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
                xbee.getResponse().getRx16Response(rx16);
          option = rx16.getOption();

          String s;
          int count = 1;
          for (int i = 0; i <  rx16.getDataLength(); i++) {
            if(rx16.getData(i)!=58){
              s += (rx16.getData(i)-48);
              //Serial.print(s);
              }
            else
            {
              //s += '\n';
              switch(count)
              {
                case 5*(BOTID-1)+ 1:
                  
                  ::r1 = s.toInt();
                  //::r1=rerange(::r1);
                  //if(::r1 < 0)
                  //  ::r1 = 3*::r1/2;
                  ::r1 = ::r1 * 2;
                  ::r1 = ::r1 - 255;
                  if(::r1 > 255){
                    ::r1 = 255;
                  }
                  if(::r1 < -255){
                    ::r1 = -255;
                  }
                  m1.mspeed(::r1);
                  //Serial.print("Wheel 1: ");
                  //Serial.print(::r1);
                  break;
                case 5*(BOTID-1)+2:
                  
                  ::r2 = s.toInt();
                  //::r2 = rerange(::r2);
                  //if(::r2 < 0)
                  //  ::r2 = 3*::r2/2;
                  ::r2 = ::r2 *2;
                  ::r2 = ::r2 - 255;
                  if(::r2 > 255){
                    ::r2 = 255;
                  }
                  if(::r2 < -255){
                    ::r2 = -255;
                  }
                  m2.mspeed(::r2);
                  //Serial.print("Wheel 2: ");
                  //Serial.print(::r2);
                  break;
                case 5*(BOTID-1)+3:
                  ::r3 = s.toInt();
                  //if(::r1 < 0)
                  //  ::r3 = 3*::r3/2;
                  ::r3 = ::r3 * 2;
                  ::r3 = ::r3 - 255;
                  if(::r3 > 255){
                    ::r3 = 255;
                  }
                  if(::r3 < -255){
                    ::r3 = -255;
                  }
                  //::r3 = rerange(::r3);
                  m3.mspeed(::r3);
                  //Serial.print("Wheel 3: ");
                  //Serial.println(::r3);
                  break;
                case 5*(BOTID-1)+4:
                  
                  ::ds = s.toInt();
                  d.mspeed(::ds);
                  //Serial.print("dribbler: ");
                  //Serial.print(ds);
                  break;
                case 5*(BOTID-1)+5:
                  
                  ::k = s.toInt();
                  if(::k == 1){
                    digitalWrite(7,HIGH);  
                  }
                  else{
                    digitalWrite(7,LOW);
                  }
                  /*Serial.print("Kicker: ");
                  Serial.println(k);*/
                  break;              
              }
              
              count++;
              s = "";
            }
           }
        }
      }
    }
    //printsp();
    //Serial.println(r1);
}
