#ifndef TIME_H
#define TIME_H

#include "Arduino.h"

class HeboTime{
    private:
        unsigned long pre_millis=0;
        int sec=0;
        int min=0;
        int hour=0;
    public:
        HeboTime();
        HeboTime(int h,int m,int s);
        void updateTime(unsigned long millis);
        void ResetTime(unsigned long millis);
        int getSec();
        int getMin();
        int getHour();
};

#endif
