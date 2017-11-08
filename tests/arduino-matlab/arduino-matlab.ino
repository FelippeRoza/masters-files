#define pin_i1 A0
#define pin_v1 A1
#define pin_i2 A2
#define pin_v2 A3
#define pin_i3 A4
#define pin_v3 A5
#define pin_rpm 2
#define pin_anem 3
#define K_SPEED 1005837.5

int val = 0;
float rpm = 0.0;
float wind_speed = 0.0;
//unsigned int rpm = 0;
//unsigned int wind_speed = 0;
volatile byte half_revolutions,pulses_anem = 0;
unsigned long timeold, timeold_anem = 0;

void rpm_gerador(){
 half_revolutions++;
}
void anem_interrupt(){
  pulses_anem++;
}

void setup() 
{
  attachInterrupt(digitalPinToInterrupt(pin_rpm),rpm_gerador, FALLING);
  attachInterrupt(digitalPinToInterrupt(pin_anem),anem_interrupt, FALLING);
  pinMode(pin_rpm, INPUT_PULLUP);
  pinMode(pin_anem, INPUT_PULLUP);
  
  Serial.begin(115200);
  Serial.println('a');
  char a = 'b';
  while (a != 'a')
  {
    a = Serial.read();
  }
}

void loop() 
{
  while (Serial.available() == 0)
  {
  }
  
  if (Serial.available() > 0)
  {
   val = Serial.read();
   if (val == 'R')
   {
     Serial.println(analogRead(pin_v1));
     Serial.println(analogRead(pin_i1));
     Serial.println(analogRead(pin_v2));
     Serial.println(analogRead(pin_i2));
     Serial.println(analogRead(pin_v3));
     Serial.println(analogRead(pin_i3));
     Serial.println(rpm);
     Serial.println(wind_speed);
   } 
  }
  delay(20);
  
  if (millis() - timeold > 1500){
    rpm = 0;
  }
  if (millis() - timeold_anem > 5000){
    wind_speed = 0;
  }
    
  if (half_revolutions >= 10) { 
    //Update RPM every 20 counts, increase this for better RPM resolution,
    //decrease for faster update
    rpm = 30*1000/(millis() - timeold)*half_revolutions;
    
    timeold = millis();
    half_revolutions = 0;
  }
  if (pulses_anem >= 5) { 
    //Update RPM every 20 counts, increase this for better RPM resolution,
    //decrease for faster update
    wind_speed = (pulses_anem*K_SPEED/((millis()-timeold_anem)*1000)); //speed in [m/s]
    
    timeold_anem = millis();
    pulses_anem = 0;
 }
}

