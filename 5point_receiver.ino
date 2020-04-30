
#include <SPI.h>
#include <AccelStepper.h>

AccelStepper stepper(1,3,2);//Step,dir
AccelStepper stepper2(1,5,4);
AccelStepper stepper3(1,7,6);
AccelStepper stepper4(1,9,8);
AccelStepper stepper5(1,11,10);

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};
int stepDest = 0;
int stepDest2 = 0;
int stepDest3 = 0;
int stepDest4 = 0;
int stepDest5 = 0;
int maxspeed = 500;
int accel = 500;

unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;


void setup() {
  Serial.begin(115200);

  delay(500);

  stepper.setMaxSpeed(maxspeed);
  stepper.setAcceleration(accel);
  stepper.moveTo(stepDest);

  stepper2.setMaxSpeed(maxspeed);
  stepper2.setAcceleration(accel);
  stepper2.moveTo(stepDest);

  stepper3.setMaxSpeed(maxspeed);
  stepper3.setAcceleration(accel);
  stepper3.moveTo(stepDest);

  stepper3.setMaxSpeed(maxspeed);
  stepper3.setAcceleration(accel);
  stepper3.moveTo(stepDest);

  stepper4.setMaxSpeed(maxspeed);
  stepper4.setAcceleration(accel);
  stepper4.moveTo(stepDest);

  stepper5.setMaxSpeed(maxspeed);
  stepper5.setAcceleration(accel);
  stepper5.moveTo(stepDest);

  //digitalWrite(7,HIGH);//half step M0


  
    // tell the PC we are ready
  //Serial.println("<Arduino is ready>");

}

void loop() {

  curMillis = millis();
 
  getDataFromPC();
  
  //updateSpeedAndAccel();
  updateStepperPos();
  
  replyToPC();

  moveSteppers();

  
  
}



void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}


void parseData() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the destination
  stepDest=atoi(strtokIndx); // 
  
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  stepDest2 = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  stepDest3 = atoi(strtokIndx);     // convert this part to another int

  strtokIndx = strtok(NULL, ","); 
  stepDest4 = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  stepDest5 = atoi(strtokIndx);
}


void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" StepDest ");
    Serial.print(stepDest);
    Serial.print(" StepDest2 ");
    Serial.print(stepDest2);
    Serial.print(" StepDest3 ");
    Serial.print(stepDest3);
    Serial.print(" StepDest4 ");
    Serial.print(stepDest4);
    Serial.print(" StepDest5 ");
    Serial.print(stepDest5);
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
}


void updateSpeedAndAccel() {
  stepper.setMaxSpeed(maxspeed);
  stepper.setAcceleration(accel);

}


void updateStepperPos() {

  stepper.moveTo(stepDest);
  stepper2.moveTo(stepDest2);
  stepper3.moveTo(stepDest3);
  stepper4.moveTo(stepDest4);
  stepper5.moveTo(stepDest5);

}



void moveSteppers() {
  stepper.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
  stepper5.run();
  }
