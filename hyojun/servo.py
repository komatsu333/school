import pigpio
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

SERVO_PIN = 4

#_init
pi = pigpio.pi()
if not pi.connected:
        exit()

def servo_angle(pi,angle,duration):
        pulse_width = int(500 + (angle / 180.0) * 2000)
        pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
        time.sleep(duration)
        pi.set_servo_pulsewidth(SERVO_PIN, 0)

if __name__ == "__main__":
        while True:
                servo_angle(pi, 120, 0.5)
                time.sleep(1)
                servo_angle(pi, 130, 0.5)
                time.sleep(1)
                servo_angle(pi, 140, 0.5)
                time.sleep(1)
                servo_angle(pi, 150, 0.5)
                time.sleep(1)
                servo_angle(pi, 140, 0.5)
                time.sleep(1)
                servo_angle(pi, 130, 0.5)
                time.sleep(1)
                servo_angle(pi, 120, 0.5)
                time.sleep(1)
                servo_angle(pi, 110, 0.5)
                time.sleep(1)
                servo_angle(pi, 100, 0.5)
                time.sleep(1)
