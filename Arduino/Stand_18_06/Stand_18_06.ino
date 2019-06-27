//Programm benötigt als Eingabe einen Buchstaben und 2 Zahlen, getrennt mit "," und beendet mit einem ";".
//Bsp.: m,3,2;
//Der Buchstabe als Befehlsaufruf, die erste Zahl als x-Koordinate, die 2. Zahl als y-Koordinate
//Die print Operationen werden im späteren Anwendungsfall nicht benötigt

#include "Arduino.h"
#include "AX12A.h"
boolean newData = false;
float xCoord;
float yCoord;
char b;
float lenD=150.0;
float lenLO=75.0;
float lenUP=150.0;
float pIntersect[4];
float angs[2];
const float pi = 3.14159265359;

#define DirectionPin  (10u)
#define BaudRate      (1000000ul)
#define IDM1            (9u)
#define IDM2            (8u)

void setup() {
  Serial.begin(9600);
  ax12a.begin(BaudRate, DirectionPin, &Serial1);
  ax12a.setMaxTorque(IDM1, 300);
  ax12a.setMaxTorque(IDM2, 300);
  newData = true;
  HomePos();
  delay(250);
  newData = false;
  Serial.println("Eingabe: Befehl(Buchstabe),x,y;");
  Serial.println("x und y Wert der Zielkoordinate");
}

void loop() {
  receiv();
  UpdateMotor();
  showNewData();
}

void receiv() {
  //Funktion zum lesen der Daten der seriellen Schnittstelle und Speichern der Werte.
  while (Serial.available() > 0 && newData == false) {

    b = Serial.readStringUntil(',')[0];
    xCoord = Serial.parseInt();
    yCoord = Serial.parseInt();

    if(Serial.read() == ';') {
      newData = true;
    }
  }       
}

float HomePos(){
  //Bewegt den den Greifer in die Home-Position.
  float xZero = 0;
  float yZero = 10;  
  getAngles(xZero, yZero);
}

float UpdateMotor(){
  //berechnet und schreibt die neuen Werte an die Motoren und bewegt anschließend den Greifer in die Ausgangsposition.
  getAngles(xCoord, yCoord);
  if(angs[0]>0){
    float AM1 = angs[0];
    float AM2 = angs[1];
    writeAngles(AM1, AM2);
    angs[0]=0;
    angs[1]=0;
    delay(1500);
    HomePos();
    delay(1500);
  }
}

float intersectCircles(float x1, float y1, float r1, float x2, float y2, float r2){
  //Funktion zur Berechnung der Schnittpunkte der Kreise um den TCP und dem jeweiligen Motor, um die benötigten Winkel der Motoren zu berechnen.
  //Mittelpunkte der zwei Kreise.
//  float p1[]={x1, y1};
//  float p2[]={x2, y2};

  //x und y Entfernung zwischen den Kreismittelpunkte.
  float dx=x2-x1;
  float dy=y2-y1;
  float distance=sqrt((dy*dy)+(dx*dx));
  
  //Entfernung zwischen den Schnittpunkten.
  float da=(((r1*r1)-(r2*r2)+(distance*distance))/(2.0*distance));
  
  //Punkt zwischen den Schnittpunkten und den Kreismittelpunkten.
  float p0x=(x1+(dx*da/distance));
  float p0y=(y1+(dy*da/distance));

  //Punkt Zwischen den Kreismittelpunkten und den Schnittpunkten.
  float p0[]={p0x, p0y};

  //Entfernung zwischen den Schnittpunkten, bzw. x/y Entfernung zwischen p0 und den Schnittpunkten.
  float h=sqrt((r1*r1)-(da*da));
  float hOffsetx=(-dx*(h/distance));
  float hOffsety=(dy*(h/distance));

  //Schnittpunkte der 2 Kreise.
  float p3x=(p0[0]-hOffsety);
  float p3y=(p0[1]-hOffsetx);
  float p4x=(p0[0]+hOffsety);
  float p4y=(p0[1]+hOffsetx);

   //Array welches zurück gegeben wird.
   pIntersect[0]=p3x;
   pIntersect[1]=p3y;
   pIntersect[2]=p4x;
   pIntersect[3]=p4y;
   return pIntersect[0];
}

float getAngles(int x, int y){
  //Funktion zum berechnen der Motorwinkel, um die Zielkoordinaten zu erreichen.
   if (newData == true) {

    //Positionen von Punkten der Kinematik, um über den Tangens Winkelwerte zu berechnen, mit welchen dann der TCP an die gewünschte Stelle bewegt wird.
    float AXaufloesung = (300.0/1024.0);
    //left motor
    float posM1[] = {(-lenD/2.0), 0.0};
    intersectCircles(x,y,lenUP,posM1[0],posM1[1],lenLO);
    float leftElbow[] = {(pIntersect[2] -posM1[0]), (pIntersect[3] -posM1[1])};
    //Winkel in RAD nach D.
    double angleM1 = atan2(leftElbow[1], leftElbow[0]);
    float angleM1D = ((angleM1*180)/pi);

    //Umrechnung von Winkel in AX Winkel und der dazugehörigen Schrittposition.
    float M1AXwinkel = angleM1D + 60;    
    float M1schrittWert = M1AXwinkel / AXaufloesung;
    
    //right motor
    float posM2[] = {(lenD/2.0), 0.0};
    intersectCircles(x,y,lenUP,posM2[0],posM2[1],lenLO);
    float rightElbow[] = {(pIntersect[0] -posM2[0]), (pIntersect[1] -posM2[1])};

    //Winkel in RAD nach D.
    double angleM2 = pi-atan2(rightElbow[1], rightElbow[0]);
    float angleM2D = ((angleM2*180)/pi);

    //Umrechnung von Winkel in AX Winkel und der dazugehörigen Schrittposition, mit dem Zusatz, dass der Winkel gespiegelt werden muss auf Grund des Aufbaus der mathematischen Berechnung.
    float M2AXwinkeln;
    float M2AXwert = angleM2D + 60;
    float M2AXwinkel = M2AXwert - 150;
    if (M2AXwinkel > 0) {
      M2AXwinkeln = 150 - M2AXwinkel;
    }
    else{
      M2AXwinkeln = 150 + (-1 * M2AXwinkel);
    }
    float M2schrittWert = M2AXwinkeln / AXaufloesung;

    //Schutz des Roboters, so dass die Kinematik keine falschen Winelwerte ansteuern kann.
//    if(M1schrittWert > 822.00 || M2schrittWert > 570.00 || M1schrittWert < 451.00 || M2schrittWert < 203.00){
//      return;
//    }

    //Winkel der beiden Motoren.
    angs[0] = M1schrittWert;
    angs[1] = M2schrittWert;
    return angs[2];
   }
}

float writeAngles(float aM1, float aM2){
  //Funktion zum schreiben von Winkelwerten auf die Servos.
  Serial.println(aM1);
  Serial.println(aM2);
  Serial.println();
  ax12a.move(IDM1, aM1);
  ax12a.move(IDM2, aM2);
}

void showNewData() {
  //Funktion zur Rückgabe der eingegebenen Werte.
    if (newData == true) {
      Serial.print("Input: ");
      Serial.println(b);
      Serial.println(xCoord);
      Serial.println(yCoord);
      Serial.println();
      newData = false;
    }
}
