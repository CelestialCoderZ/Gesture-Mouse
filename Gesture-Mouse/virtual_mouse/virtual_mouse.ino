// Arduino reads distances from 2 ultrasonic sensors and sends "d1,d2" over Serial

const int trig1 = 2, echo1 = 3;
const int trig2 = 4, echo2 = 5;

long readDistance(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH, 30000); // timeout
  if (duration == 0) return 999;  // no echo
  return duration / 58;           // convert to cm
}

void setup() {
  pinMode(trig1, OUTPUT); pinMode(echo1, INPUT);
  pinMode(trig2, OUTPUT); pinMode(echo2, INPUT);
  Serial.begin(115200);
}

void loop() {
  long d1 = readDistance(trig1, echo1);
  long d2 = readDistance(trig2, echo2);
  Serial.print(d1);
  Serial.print(",");
  Serial.println(d2);
  delay(50);
}


