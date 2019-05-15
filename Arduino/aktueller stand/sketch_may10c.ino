//problem: aufnehmen der werte von der intesectcircles funktion(pIntersect)

//Programm benötigt als Eingabe einen Buchstaben und 2 Zahlen, getrennt mit "," und beendet mit einem ";".
//Bsp.: m,3,2;
//Der Buchstabe als Befehlsaufruf, die erste Zahl als x-Koordinate, die 2. Zahl als y-Koordinate
//Die print Operationen werden im späteren Anwendungsfall nicht benötigt

boolean newData = false;
float xCoord;
float yCoord;
char c;
float lenD=500.0;
float lenLO=150.0;
float lenUP=300.0;
float angs[2];
float angleM1[1];
float angleM2[1];
//float elbowLeftIntersections[3];
//float elbowRightIntersections[3];
float pIntersect[4];
const float pi = 3.14159265359;

void setup() {
  Serial.begin(9600);
  Serial.println("Befehl(Buchstabe),x,y; Coords?");
}

void loop() {
  receiv();
  getAngles();
  showNewData();
}

void receiv() {
  static byte anzahl = 0;

  while (Serial.available() > 0 && newData == false) {

    c = Serial.readStringUntil(',')[0];
    xCoord = Serial.parseInt();
    yCoord = Serial.parseInt();

    if(Serial.read() == ';') {
      newData = true;
    }
  }       
}

void showNewData() {
    if (newData == true) {
      Serial.print("Input: ");
      Serial.println(c);
      Serial.println(xCoord);
      Serial.println(yCoord);
//      Serial.println(angs[0]);
//      Serial.println(angs[1]);
//      Serial.println(angleM1);
//      Serial.println(angleM2[0]);
      newData = false;
    }
}

float intersectCircles(float x1, float x2, float y1, float y2, float r1, float r2){
  
  //Mittelpunkte der zwei Kreise.
  float p1[]={x1, y1};
  float p2[]={x2, y2};
  
  //x und y Entfernung zwischen den Kreismittelpunkte.
  float dx=x2-x1;
  float dy=y2-y1;
  
  float distance=sqrt((dy*dy)+(dx*dx));
  
  float da=(((r1*r1)-(r2*r2)+(distance*distance))/(2.0*distance));
  
  //Punkt zwischen den Schnittpunkten und den kreismittelpunkten.
  float p0x=(x1+(dx*da/distance));
  float p0y=(y1+(dy*da/distance));
  
  float p0[]={p0x, p0y};
  
  float h=sqrt((da*da)-(r2*r2)); //eigentlich müsste r2-da ?
  
  //Entfernung zwischen p0 und den Schnittpunkten.
  float hOffsetx=(-dy*(h/distance));
  float hOffsety=(dy*(h/distance));
  
  float p3x=(p2[0]+hOffsetx);
  float p3y=(p2[1]+hOffsetx);
  float p4x=(p2[0]-hOffsetx);
  float p4y=(p2[1]-hOffsetx);

  //IntersectionPoints der 2 Kreise.
   pIntersect[0]=p3x;
   pIntersect[1]=p3y;
   pIntersect[2]=p4x;
   pIntersect[3]=p4y;
//   Serial.println(pIntersect[2]);
   return pIntersect[0];
}

float getAngles(){
   //GETMOTORANGLES Summary of this function goes here
   //   Detailed explanation goes here
   if (newData == true) {
    
    //left motor
    float posM1[] = {(-lenD/2.0), 0.0};
    intersectCircles(xCoord,yCoord,lenUP,posM1[0],posM1[1],lenLO);
    float leftElbow[] = {(pIntersect[3] -posM1[0]), (pIntersect[4] -posM1[1])};
    
    double angleM1 = atan2(leftElbow[1], leftElbow[0]); //dY,dX
       
    //right motor
    float posM2[] = {(lenD/2.0), 0.0};
    intersectCircles(xCoord,yCoord,lenUP,posM2[0],posM2[1],lenLO);
    float rightElbow[] = {(pIntersect[0] -posM2[0]), (pIntersect[1] -posM2[1])};
     
    double angleM2 = (180-atan2(rightElbow[1],rightElbow[0])); //dY,dX
     
    float angs[] = {angleM1, angleM2};
    Serial.println(angs[0]);
    Serial.println(angs[1]);
   }
}
