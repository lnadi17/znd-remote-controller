// Define stepper motor connections and steps per revolution:
#define dirPinX 2
#define stepPinX 3
#define dirPinY 4
#define stepPinY 5
#define stepsPerRevolution 200

#define stepsPerMmX 5
#define stepsPerMmY 5

#define motorY 1
#define motorX 0

#define clockwise 1
#define counterClockwise 0

void moveX(int mm) {
  if(!mm) return;
  for(int i = 0; i < stepsPerMmX * abs(mm); i++)
      oneStep(mm > 0 ? clockwise : counterClockwise, motorX);
}

void moveY(int mm) {
   if(!mm) return;
   for(int i = 0; i < stepsPerMmY * abs(mm); i++)
      oneStep(mm > 0 ? clockwise : counterClockwise, motorY);
}

void oneStep(int dir, int n) {
  // set direction
  digitalWrite(n ? dirPinY : dirPinX, dir);
  // spin
  int stepPin = n ? stepPinY : stepPinX;
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(100000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(100000);
}

void setup() {
  Serial.begin(9600);
  // Declare pins as output:
  pinMode(stepPinX, OUTPUT);
  pinMode(dirPinX, OUTPUT);
  pinMode(stepPinY, OUTPUT);
  pinMode(dirPinY, OUTPUT);
  moveY(200);
  moveX(-200);
}

void loop() {
  // read from serial
//  if(movex)
//    moveX(xmm);
//    Serial.print("X moved~");
//  else if(movey)
//    moveY(ymm);
//    Serial.print("Y moved~");
//  moveX(20);
}
