/*  新しい本体に変更のためスピードの値を調整  10/15
 *  ライン走行中に停止ボタンをおすと停止　10/21
 *  スイッチがONになるのを検知 11/06
 *  前輪を別のモータードライバーで操作 11/14
 *  チャタリングを除去 11/18
 *  417行目の while をコメントアウト -> wifi繋がらないため　11/22
 *    -> 電源をつなげてリセットすると解決
 *  スイッチ3つ １つめは前進　2つ目は押して5sで起動 　３つめは停止   11/22
 *  ライントレースできるように 
 *  スマホで操作　＆　スイッチ３つで操作できるように  11/25
 *  操作準備完了時にLEDが点灯するように 2/3
 */


#include <Servo.h>
#include "HeboTime.h"
HeboTime time;
char buffer[30];

#define TURN_SPEED 200  
#define SPEED  255    
#define SHIFT_SPEED 130  

#define TURN_TIME 500  
#define MOVE_TIME 500  

#define speedPinR 9                               //  RIGHT WHEEL PWM pin D45 connect front MODEL-X ENA 
#define RightMotorDirPin1  22                     //Front Right Motor direction pin 1 to Front MODEL-X IN1  (K1)
#define RightMotorDirPin2  24                     //Front Right Motor direction pin 2 to Front MODEL-X IN2   (K1)                                 
#define LeftMotorDirPin1  26                      //Left front Motor direction pin 1 to Front MODEL-X IN3 (  K3)
#define LeftMotorDirPin2  28                     //Left front Motor direction pin 2 to Front MODEL-X IN4 (  K3)
#define speedPinL 10                              // Left WHEEL PWM pin D7 connect front MODEL-X ENB

#define speedPinRB 11   //  RIGHT WHEEL PWM pin connect Back MODEL-X ENA 
#define RightMotorDirPin1B  5    //Rear Right Motor direction pin 1 to Back MODEL-X IN1 (  K1)
#define RightMotorDirPin2B 6    //Rear Right Motor direction pin 2 to Back MODEL-X IN2 (  K1) 
#define LeftMotorDirPin1B 7    //Rear left Motor direction pin 1 to Back MODEL-X IN3  K3
#define LeftMotorDirPin2B 8  //Rear left Motor direction pin 2 to Back MODEL-X IN4  k3
#define speedPinLB 12    //   LEFT WHEEL  PWM pin D8 connect Rear MODEL-X ENB


#define SERVO_PIN     13  //servo connect to D5
#define Echo_PIN    31 // Ultrasonic Echo pin connect to A5
#define Trig_PIN    30  // Ultrasonic Trig pin connect to A4

#define MID_SPEED 100*3/4    
#define HIGH_SPEED 120*3/4
#define LOW_SPEED 90*3/4
#define LONG_DELAY_TIME 110*3/4  
#define DELAY_TIME 40  
#define SHORT_DELAY_TIME 70*3/4   
         
#define speedPinR 9   //50  Front Wheel PWM pin connect Right MODEL-X ENA 
#define RightMotorDirPin1  22    //48 Front Right Motor direction pin 1 to Right MODEL-X IN1  (K1)
#define RightMotorDirPin2  24   //42  Front Right Motor direction pin 2 to Right MODEL-X IN2   (K1)                                 
#define LeftMotorDirPin1  26    //44  Front Left Motor direction pin 1 to Right MODEL-X IN3 (K3)
#define LeftMotorDirPin2  28   //46 Front Left Motor direction pin 2 to Right MODEL-X IN4 (K3)
#define speedPinL 10   //52  Front Wheel PWM pin connect Right MODEL-X ENB

#define speedPinRB 11   //  Rear Wheel PWM pin connect Left MODEL-X ENA 
#define RightMotorDirPin1B  5    //Rear Right Motor direction pin 1 to Left  MODEL-X IN1 ( K1)
#define RightMotorDirPin2B 6    //Rear Right Motor direction pin 2 to Left  MODEL-X IN2 ( K1) 
#define LeftMotorDirPin1B 7    //Rear Left Motor direction pin 1 to Left  MODEL-X IN3  (K3)
#define LeftMotorDirPin2B 8  //Rear Left Motor direction pin 2 to Left  MODEL-X IN4 (K3)
#define speedPinLB 12    //  Rear Wheel PWM pin connect Left MODEL-X ENB
#define sensor1   A4 // Left most sensor
#define sensor2   A3 // 2nd Left   sensor
#define sensor3   A2 // center sensor
#define sensor4   A1 // 2nd right sensor
#define sensor5   A0 // Right most sensor
#define SERVO_PIN     13  //servo connect to D5
#define Echo_PIN    31 // Ultrasonic Echo pin connect to A5
#define Trig_PIN    30  // Ultrasonic Trig pin connect to A4

#define FAST_SPEED  110  //both sides of the motor speed
#define R_SPEED  165   //both sides of the motor speed


#define FORWARD_TIME 200   //前進距離
#define BACK_TIME  300  // 後方距離
#define TURN_TIME  250  //ロボットが回転するのに費やした時間 (ミリ秒)
#define OBSTACLE_LIMIT 30  //minimum distance in cm to obstacles at both sides (the car will allow a shorter distance sideways)  両側の障害物までの最小距離 (cm) (車は横方向にこれより短い距離を許可します)

#define s00 0  //Module pins wiring
#define s01 1
#define s02 2
#define s03 3
#define out 4

#define bt_sw 53    //ON,OFF切り替えスイッチ
#define bt_time 51  //おすと5s後にきどうするスイッチ
#define bt_stop 49  //おすと停止

#define led_ok 52   //操作準備完了LED
#define led_red 46
#define led_green 48
#define led_yeloow 50

int Red=0, Blue=0, Green=0; //RGB values
int data = 0;  //This is where we're going to stock our values

int distance;
Servo head;

const int buttonPin = 32;     // スイッチ入力ピン
/*motor control*/
void forward(int speed_left,int speed_right)
{
   RL_fwd(speed_left);
   RR_fwd(speed_right);
   FR_fwd(speed_right);
   FL_fwd(speed_left); 
}
void reverse(int speed)
{
   RL_bck(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_bck(speed); 
}
void right_shift(int speed_fl_fwd,int speed_rl_bck ,int speed_rr_fwd,int speed_fr_bck) {
  FL_fwd(speed_fl_fwd); 
  RL_bck(speed_rl_bck); 
  FR_bck(speed_fr_bck);
  RR_fwd(speed_rr_fwd);
;
}
void left_shift(int speed_fl_bck,int speed_rl_fwd ,int speed_rr_bck,int speed_fr_fwd){
   FL_bck(speed_fl_bck);
   RL_fwd(speed_rl_fwd);
   FR_fwd(speed_fr_fwd);
   RR_bck(speed_rr_bck);
  
}
void go_advance(int speed){
   RL_fwd(speed);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_fwd(speed); 
}
void go_advance_half(int speed){
   RL_fwd(speed);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_fwd(speed); 
}
void  go_back(int speed){
   RL_bck(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_bck(speed); 
}
void left_turn(int speed){
   RL_bck(0);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_bck(0); 
}
void right_turn(int speed){
   RL_fwd(speed);
   RR_bck(0);
   FR_bck(0);
   FL_fwd(speed); 
}
void around(int speed){
   RL_fwd(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_fwd(speed);
}
void left_back(int speed){
   RL_fwd(0);
   RR_bck(speed);
   FR_bck(speed);
   FL_fwd(0); 
}
void right_back(int speed){
   RL_bck(speed);
   RR_fwd(0);
   FR_fwd(0);
   FL_bck(speed); 
}

void right(int speed)
{
   RL_fwd(speed);
   RR_bck(0);
   FR_bck(0);
   FL_fwd(speed); 
}
void left(int speed)
{
   RL_fwd(0);
   RR_bck(speed);
   FR_bck(speed);
   FL_fwd(0); 
}
void sharpRightTurn(int speed_left,int speed_right)
{
   RL_fwd(speed_left);
   RR_bck(speed_right);
   FR_bck(speed_right);
   FL_fwd(speed_left); 
}
void sharpLeftTurn(int speed_left,int speed_right){
   RL_bck(speed_left);
   RR_fwd(speed_right);
   FR_fwd(speed_right);
   FL_bck(speed_left); 
}

void clockwise(int speed){
   RL_fwd(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_fwd(speed); 
}
void countclockwise(int speed){
   RL_bck(speed);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_bck(speed); 
}
void FR_bck(int speed)  //front-right wheel forward turn
{
  digitalWrite(RightMotorDirPin1, HIGH);
  digitalWrite(RightMotorDirPin2,LOW); 
  analogWrite(speedPinR,speed);
}
void FR_fwd(int speed) // front-right wheel backward turn
{
  digitalWrite(RightMotorDirPin1,LOW);
  digitalWrite(RightMotorDirPin2,HIGH); 
  analogWrite(speedPinR,speed);
}
void FL_bck(int speed) // front-left wheel forward turn
{
  digitalWrite(LeftMotorDirPin1,HIGH);
  digitalWrite(LeftMotorDirPin2,LOW);
  analogWrite(speedPinL,speed);
}
void FL_fwd(int speed) // front-left wheel backward turn
{
  digitalWrite(LeftMotorDirPin1,LOW);
  digitalWrite(LeftMotorDirPin2,HIGH);
  analogWrite(speedPinL,speed);
}

void RR_bck(int speed)  //rear-right wheel forward turn
{
  digitalWrite(RightMotorDirPin1B, HIGH);
  digitalWrite(RightMotorDirPin2B,LOW); 
  analogWrite(speedPinRB,speed);
}
void RR_fwd(int speed)  //rear-right wheel backward turn
{
  digitalWrite(RightMotorDirPin1B, LOW);
  digitalWrite(RightMotorDirPin2B,HIGH); 
  analogWrite(speedPinRB,speed);
}
void RL_bck(int speed)  //rear-left wheel forward turn
{
  digitalWrite(LeftMotorDirPin1B,HIGH);
  digitalWrite(LeftMotorDirPin2B,LOW);
  analogWrite(speedPinLB,speed);
}
void RL_fwd(int speed)    //rear-left wheel backward turn
{
  digitalWrite(LeftMotorDirPin1B,LOW);
  digitalWrite(LeftMotorDirPin2B,HIGH);
  analogWrite(speedPinLB,speed);
}
 
void stop_Stop()    //Stop
{
  digitalWrite(RightMotorDirPin1, LOW);
  digitalWrite(RightMotorDirPin2,LOW);
  digitalWrite(LeftMotorDirPin1,LOW);
  digitalWrite(LeftMotorDirPin2,LOW);
  digitalWrite(RightMotorDirPin1B, LOW);
  digitalWrite(RightMotorDirPin2B,LOW);
  digitalWrite(LeftMotorDirPin1B,LOW);
  digitalWrite(LeftMotorDirPin2B,LOW);
  set_Motorspeed(0,0,0,0);
}
/*set motor speed */
void set_Motorspeed(int leftFront,int rightFront,int leftBack,int rightBack)
{
  analogWrite(speedPinL,leftFront); 
  analogWrite(speedPinR,rightFront); 
 analogWrite(speedPinLB,leftBack);  
 analogWrite(speedPinRB,rightBack);

}
/*超音波距離の検出*/
int watch(){
  long echo_distance;
  digitalWrite(Trig_PIN,LOW);
  delayMicroseconds(5);                                                                              
  digitalWrite(Trig_PIN,HIGH);
  delayMicroseconds(15);
  digitalWrite(Trig_PIN,LOW);
  echo_distance=pulseIn(Echo_PIN,HIGH);
  echo_distance=echo_distance*0.01657; //物体までの距離は何cmですか
 //Serial.println((int)echo_distance);
  return round(echo_distance);
}

//左、中央、右までの距離を測定
String watchsurrounding(){
/*  object_status は 2 進整数で、最後の 3 桁は左前方、真正面、右前方に障害物があるかどうかを表します。
 ※3桁の文字列、例：100は左前方に障害物があることを意味し、011は真正面と右前方に障害物があることを意味します
*/
  int obstacle_status =B1000;
  head.write(160); //センフォルは左前方向を向いています
  delay(1);
  distance = watch();
  if(distance<OBSTACLE_LIMIT){
    stop_Stop();
    
     obstacle_status  =obstacle_status | B100;
    }
  head.write(90); //セソルは真正面を向いています
  delay(1);
  distance = watch();
  if(distance<OBSTACLE_LIMIT){
    stop_Stop();
    
    obstacle_status  =obstacle_status | B10;
    }

  head.write(20); //センサーは右前方20度方向を向いています
  delay(1);
  distance = watch();
  if(distance<OBSTACLE_LIMIT){
    stop_Stop();
    
    obstacle_status  =obstacle_status | 1;
    }

   String obstacle_str= String(obstacle_status,BIN);
  obstacle_str= obstacle_str.substring(1,4);
  
  return obstacle_str; //5 方向の障害物ステータスを表す 5 文字の文字列を返します。
}

void auto_avoidance(){
 String obstacle_sign=watchsurrounding(); // 5 桁の障害物サインのバイナリ値は 5 方向の障害物の状態を意味します
 Serial.print("begin str=");
 Serial.println(obstacle_sign);
 if(  obstacle_sign=="111" || obstacle_sign=="101" || obstacle_sign=="001"|| obstacle_sign=="010"|| obstacle_sign=="011" || obstacle_sign=="100"|| obstacle_sign=="110"){
    Serial.println("--------------------------");
    stop_Stop();
    set_Motorspeed(0,0,0,0);
    //delay(BACK_TIME);
    //stop_Stop();
   } 
}

 
void stop_bot()    //Stop
{
  analogWrite(speedPinLB,0);
  analogWrite(speedPinRB,0);
  analogWrite(speedPinL,0);
  analogWrite(speedPinR,0);
  digitalWrite(RightMotorDirPin1B, LOW);
  digitalWrite(RightMotorDirPin2B,LOW);   
  digitalWrite(LeftMotorDirPin1B, LOW);
  digitalWrite(LeftMotorDirPin2B,LOW); 
  digitalWrite(RightMotorDirPin1, LOW);
  digitalWrite(RightMotorDirPin2,LOW);   
  digitalWrite(LeftMotorDirPin1, LOW);
  digitalWrite(LeftMotorDirPin2,LOW); 
  delay(40);
}
//Pins initialize
void init_GPIO()
{
  pinMode(RightMotorDirPin1, OUTPUT); 
  pinMode(RightMotorDirPin2, OUTPUT); 
  pinMode(speedPinL, OUTPUT);  
 
  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT); 
  pinMode(speedPinR, OUTPUT);
  pinMode(RightMotorDirPin1B, OUTPUT); 
  pinMode(RightMotorDirPin2B, OUTPUT); 
  pinMode(speedPinLB, OUTPUT);  
 
  pinMode(LeftMotorDirPin1B, OUTPUT);
  pinMode(LeftMotorDirPin2B, OUTPUT); 
  pinMode(speedPinRB, OUTPUT);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(sensor3, INPUT);
  pinMode(sensor4, INPUT);
  pinMode(sensor5, INPUT);

  stop_Stop();
}

#include "WiFiEsp.h"
#include "WiFiEspUDP.h"
char ssid[] = "osoyoo_robot"; 

int status = WL_IDLE_STATUS;
// use a ring buffer to increase speed and reduce memory allocation
 char packetBuffer[5]; 
WiFiEspUDP Udp;
unsigned int localPort = 8888;  // local port to listen on
void setup()
{ 
 init_GPIO();
  Serial.begin(9600);   // initialize serial for debugging
    Serial1.begin(115200);
    Serial1.write("AT+UART_DEF=9600,8,1,0,0\r\n");
  delay(200);
  Serial1.write("AT+RST\r\n");
  delay(200);
  Serial1.begin(9600);    // initialize serial for ESP module
  WiFi.init(&Serial1);    // initialize ESP module

  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    //while (true);
  }

    Serial.print("Attempting to start AP ");
   Serial.println(ssid);
   //AP mode
   status = WiFi.beginAP(ssid, 10, "", 0);

  Serial.println("You're connected to the network");
  printWifiStatus();
  Udp.begin(localPort);
  
  Serial.print("Listening on port ");
  Serial.println(localPort);
  pinMode(RightMotorDirPin1, OUTPUT); 
  pinMode(RightMotorDirPin2, OUTPUT); 
  pinMode(speedPinL, OUTPUT);  
 
  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT); 
  pinMode(speedPinR, OUTPUT);
  pinMode(RightMotorDirPin1B, OUTPUT); 
  pinMode(RightMotorDirPin2B, OUTPUT); 
  pinMode(speedPinLB, OUTPUT);  
 
  pinMode(LeftMotorDirPin1B, OUTPUT);
  pinMode(LeftMotorDirPin2B, OUTPUT); 
  pinMode(speedPinRB, OUTPUT);
  stop_Stop();//stop move
  /*init HC-SR04*/
  pinMode(Trig_PIN, OUTPUT); 
  pinMode(Echo_PIN,INPUT); 
  /*init buzzer*/
 
  digitalWrite(Trig_PIN,LOW);
  /*init servo*/
  head.attach(SERVO_PIN); 

  head.write(90);
   delay(200);
  
  pinMode(s00, OUTPUT);  //pin modes
  pinMode(s01, OUTPUT);
  pinMode(s02, OUTPUT);
  pinMode(s03, OUTPUT);
  pinMode(out, INPUT);
   
  digitalWrite(s00, HIGH);  //Putting S0/S1 on HIGH/HIGH levels means the output frequency scalling is at 100% (recommended)
  digitalWrite(s01, HIGH);  //LOW/LOW is off HIGH/LOW is 20% and LOW/HIGH is 2%

  Serial.begin(9600);
 
  pinMode(bt_sw, INPUT);
  pinMode(bt_time, INPUT);
  pinMode(bt_stop, INPUT);
  pinMode(led_ok, OUTPUT);
  pinMode(led_red, OUTPUT);
  pinMode(led_green, OUTPUT);
  pinMode(led_yeloow, OUTPUT);
 
  stop_Stop();//Stop
}

int packetSize = Udp.parsePacket();
int while_cnt = 0;

int status_sw = 0;
int buttonState1 = 1;
int buttonState2 = 1;
int buttonState3 = 1;
int loopcnt = 0;

int set_time = -1;
int Hour_int = 0;
String Hour_str;
int Min_int = 0;
String Min_str;
int Sec_int = 0;
String Sec_str;


void loop()
{
  digitalWrite(led_ok, HIGH);
  time.updateTime(millis());//更新してあげないと動かないヘボ仕様

  Hour_str = time.getMin();     //時間の値を取得
  Hour_int = Min_str.toInt();
  Min_str = time.getMin();      //分の値を取得
  Min_int = Min_str.toInt();
  Sec_str = time.getSec();      //秒の値を取得
  Sec_int = Sec_str.toInt();

  buttonState1 = digitalRead(bt_sw);      //ボタン1を取得
  buttonState2 = digitalRead(bt_time);    //ボタン2を取得
  buttonState3 = digitalRead(bt_stop);    //ボタン3を取得

  if (buttonState1 == LOW && loopcnt == 0) {       //スイッチが押されたとき LOW（プルアップなので逆）
    status_sw ^= 1;
    loopcnt = 1;
    if(status_sw){
      go_advance(SPEED);
    } else {
    stop_Stop();
    }
  }else if  (buttonState1 == HIGH){
    loopcnt = 0;
  }

  if (buttonState2 == LOW) {        //プルアップなので逆
    //Line_cmd();    
    go_advance_half(SHIFT_SPEED);               
  }

  if (buttonState3 == LOW) {
    status_sw = 0;
    stop_Stop();
  }

  if(Sec_int == set_time){              
    time.ResetTime(millis());
    go_advance(TURN_SPEED);
    set_time = -1;
  }
  
  packetSize = Udp.parsePacket();
  if (packetSize) {                               // if you get a client,
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    int len = Udp.read(packetBuffer, 255);
   if (len > 0) {
      packetBuffer[len] = 0;
    }
      char c=packetBuffer[0];
      switch (c)    //serial control instructions
      {  
        case 'B':go_back(SPEED);break;    //↓　B
        case 'L':left_turn(TURN_SPEED);break;//←　L
        case 'R':right_turn(TURN_SPEED);break;//→　R
        case 'A':go_advance(TURN_SPEED);break;//↑　A     //SPEED
        case 'E':stop_Stop();break;//＝　W
        case 'F':left_shift(0,150,0,150);break; //F1
        case 'H':right_shift(180,0,150,0);break; //F3
        case 'I':left_shift(150,0,150,0); break;//F5
        case 'K':right_shift(0,130,0,130); break;//F6
        case 'O':left_shift(200,150,150,200); break;//obstacle
        case 'T':right_shift(200,200,200,200); break;//tracking

        case 'G':Line_cmd();//F2
                 break;

        case 'J':around(TURN_SPEED);break;//F5
        default:break;
      }
    }
}

void Line_cmd(){
  while_cnt=0;
  Line();//F2
  if(while_cnt==1){
    while_cnt=0;
  }
}
void Line(){
  while(while_cnt == 0){
    tracking();
    auto_avoidance();
    Serial.println(">>>>>>>>>>>>");
    Serial.println(while_cnt);
    Serial.println("<<<<<<<<<<<<");
  }
}

void tracking()
{
  String obstacle_sign=watchsurrounding(); // 5 桁の障害物サインのバイナリ値は 5 方向の障害物の状態を意味します
  String senstr="";
  int s0 = !digitalRead(sensor1);
  int s1 = !digitalRead(sensor2);
  int s2 = !digitalRead(sensor3);
  int s3 = !digitalRead(sensor4);
  int s4 = !digitalRead(sensor5);
  int sensorvalue=32;
  sensorvalue +=s0*16+s1*8+s2*4+s3*2+s4;
  senstr= String(sensorvalue,BIN);
  senstr=senstr.substring(1,6);
  
  Serial.print(senstr);
  Serial.print("\t");
 
  if ( senstr=="10000" || senstr=="01000" || senstr=="11000"){
    if(obstacle_sign=="000"){
      Serial.println(" Shift Left");
      sharpLeftTurn(LOW_SPEED,MID_SPEED);
    }
  }
   
  if ( senstr=="11100" || senstr=="10100"){
    if(obstacle_sign=="000"){    
      Serial.println("Slight Shift Left");
      sharpLeftTurn(LOW_SPEED,MID_SPEED);
      delay(DELAY_TIME);
    }
  }

  if ( senstr=="01100" ||  senstr=="11110"  || senstr=="10010"  || senstr=="10110"  || senstr=="11010"){
    if(obstacle_sign=="000"){
      Serial.println("Slit Right");
      forward(LOW_SPEED,LOW_SPEED);
    }
  }

  if (senstr=="01110" || senstr=="01010" || senstr=="00100"  || senstr=="10001"  || senstr=="10101"  || senstr=="10011" || senstr=="11101" || senstr=="10111" || senstr=="11011"  || senstr=="11001"){
    if(obstacle_sign=="000"){
      Serial.println("Forward");
      forward(LOW_SPEED,LOW_SPEED);
    }
  }

  if ( senstr=="00110" || senstr=="01111" || senstr=="01001" || senstr=="01011" || senstr=="01101"){
    if(obstacle_sign=="000"){
      Serial.println("Slight Left");
      forward(LOW_SPEED,LOW_SPEED);
    }
  }

  if (senstr=="00111" || senstr=="00101"){
    if(obstacle_sign=="000"){
     Serial.println("Slight Shift to Right ");
     sharpRightTurn(MID_SPEED,LOW_SPEED);
     delay(DELAY_TIME);
    } 
  }

  if (senstr=="00001" || senstr=="00010" || senstr=="00011"){
    if(obstacle_sign=="000"){
     Serial.println("Shift to Right");
     sharpRightTurn(MID_SPEED,LOW_SPEED);
    }
  }
  if (  senstr=="00000"){
    Serial.println("-------------Stop------------");
    sharpRightTurn(0,0);
    while_cnt = 1;  
 }
 if (  senstr=="11111"){
  Serial.println(obstacle_sign);
  if(obstacle_sign=="000"){
    //forward(TURN_SPEED,TURN_SPEED);
    go_advance(TURN_SPEED);
  }
 }
  digitalWrite(s2, LOW);  //S2/S3 levels define which set of photodiodes we are using LOW/LOW is for RED LOW/HIGH is for Blue and HIGH/HIGH is for green
  digitalWrite(s3, LOW);
  Serial.print("Red value= ");
  GetData();  //Executing GetData function to get the value

  digitalWrite(s2, LOW);
  digitalWrite(s3, HIGH);
  Serial.print("Blue value= ");
  GetData();

  digitalWrite(s2, HIGH);
  digitalWrite(s3, HIGH);
  Serial.print("Green value= ");
  GetData();

  Serial.println();

  GetColors(); //Execute the GetColors function to get the value of each RGB color
  //Depending of the RGB values given by the sensor we can define the color and displays it on the monitor

  if (Red >=50 && Green >=50 && Blue >=50){
   Serial.println("Black");
   left_shift(0,150,0,150);
   delay(20);
//   stop_Stop();
//   while_cnt = 1;
  }else if (Red <=15 && Green <=15 && Blue <=15){ //If the values are low it's likely the white color (all the colors are present)
    Serial.println("White");

  }else if (Red<Blue && Red<=Green && Red<23){ //if Red value is the lowest one and smaller thant 23 it's likely Red
    Serial.println("Red");

  }else if (Blue<Green && Blue<Red && Blue<20){ //Same thing for Blue
    Serial.println("Blue");

  }else if (Green<Red && Green-Blue<= 8){ //Green it was a little tricky, you can do it using the same method as above (the lowest), but here I used a reflective object
    Serial.println("Green"); //which means the blue value is very low too, so I decided to check the difference between green and blue and see if it's acceptable

  }else{
    Serial.println("Unknown"); //if the color is not recognized, you can add as many as you want
  }
}
 

void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}

void GetData() {
  data = pulseIn(out, LOW);  //here we wait until "out" go LOW, we start measuring the duration and stops when "out" is HIGH again
  Serial.print(data);        //it's a time duration measured, which is related to frequency as the sensor gives a frequency depending on the color
  Serial.print("\t");        //The higher the frequency the lower the duration
  delay(20);
}

void GetColors()
{
digitalWrite(s02, LOW); //S2/S3 levels define which set of photodiodes we are using LOW/LOW is for RED LOW/HIGH is for Blue and HIGH/HIGH is for green
digitalWrite(s03, LOW);
Red = pulseIn(out, digitalRead(out) == HIGH ? LOW : HIGH); //here we wait until "out" go LOW, we start measuring the duration and stops when "out" is HIGH again, if you have trouble with this expression check the bottom of the code
delay(20);
digitalWrite(s03, HIGH); //Here we select the other color (set of photodiodes) and measure the other colors value using the same techinque
Blue = pulseIn(out, digitalRead(out) == HIGH ? LOW : HIGH);
delay(20);
digitalWrite(s02, HIGH);
Green = pulseIn(out, digitalRead(out) == HIGH ? LOW : HIGH);
delay(20);
}
