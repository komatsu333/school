#include "Arduino.h"
#include "HeboTime.h"


HeboTime::HeboTime(){}
HeboTime::HeboTime(int h,int m,int s){
    sec = s;
    min = m;
    hour= h;
}
void HeboTime::updateTime(unsigned long millis){
    //算出
  if(millis-pre_millis >= 1000){
    Serial.print(millis);
    Serial.print(":");
    Serial.println(pre_millis);
    sec += (millis-pre_millis)/1000;//経過秒数分加算
    pre_millis=millis;//更新
    if(sec>=60){//60秒超えたらsec,minを更新
      min += sec/60;
      sec=sec%60;//更新
      if(min>=60){//60分超えたらmin,hour
        hour+=min/60;
        min=min%60;//更新
      }
    }
  }
  //millisがデータ範囲(4,294,967,295)を超えてリセットされたら
  if(millis<pre_millis){
    pre_millis=0;//TODO：ここでずれが生じるのをどうにかせねば
  }
}

void HeboTime::ResetTime(unsigned long millis){
  sec = 0;
  min = 0;
  hour = 0;
}

int HeboTime::getSec(){
    return sec;
}
int HeboTime::getMin(){
    return min;
}
int HeboTime::getHour(){
    return hour;
}
