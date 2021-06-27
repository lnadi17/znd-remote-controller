// Define stepper motor connections and steps per revolution
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

int currentX;
int currentY;

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
  // Set direction
  digitalWrite(n ? dirPinY : dirPinX, dir);
  // Spin
  int stepPin = n ? stepPinY : stepPinX;
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(100000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(100000);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Program started.");
  Serial.println("=====================");
  Serial.println("Available commands:\n1. movex\n2. movey");
  Serial.println("=====================~");
  // Declare pins as output
  pinMode(stepPinX, OUTPUT);
  pinMode(dirPinX, OUTPUT);
  pinMode(stepPinY, OUTPUT);
  pinMode(dirPinY, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readString();
    Serial.println(data);
    if (getValue(data, ' ', 0) == "movex") {
      int moveValue = getValue(data, ' ', 1).toInt();
      moveX(moveValue);
    } else if (getValue(data, ' ', 0) == "movey") {
      int moveValue = getValue(data, ' ', 1).toInt();
      moveY(moveValue);
    } else {
      Serial.print("Unknown command.");
    }
    Serial.println("~");
  }
}

String getValue(String data, char separator, int index) {
  int wordIndex = -1;
  int startIndex = 0;
  int endIndex = -1;
  int maxIndex = data.length() - 1;
  
  for (int i = 0; i <= maxIndex; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      endIndex = (i == maxIndex) ? i + 1 : i;
      if (++wordIndex == index) {
        return data.substring(startIndex, endIndex);
      } else {
        startIndex = endIndex + 1;
      }
    }
  }
}
