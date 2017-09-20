#include <PWM.h>

int pin_out = 45;
int input = 0;
int output = 0;

void setup()
{
  //initialize all timers except for 0, to save time keeping functions
 //just because you init the timer doesn't change the default frequency until you call setpinfreq 
 InitTimersSafe(); 

  //sets the frequency for the specified pin
  bool success = SetPinFrequencySafe(pin_out, 20000);
  //success == true if it worked
  Serial.begin(9600);
}

void loop()
{
  //or you can set it in the loop at anytime
  if (Serial.available() > 0) {
          // read the incoming byte:
          input = Serial.parseInt();
  
          // say what you got:
          Serial.println(input, DEC);
  }
  output = map(input, 0, 100, 0, 400);
  analogWrite(pin_out, output);
  delay(30);
}
