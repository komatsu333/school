import pigpio
from time import sleep

# モーターピン
RIGHT_IN1 = 2
RIGHT_IN2 = 3
LEFT_IN1 = 5
LEFT_IN2 = 6

# デューティー比
DUTY_CV = 2
DUTY_DIAGONAL = 30

# 速度設定(1～255)
MAX_SPEED = 26     # 最高速度
MIN_SPEED = 6      # 最低速度
low_speed = 8      # 低速
high_speed = 20    # 高速
turn_speed = 12

def init_mortor(pi):
    pi.set_mode(RIGHT_IN1, pigpio.OUTPUT)
    pi.set_mode(RIGHT_IN2, pigpio.OUTPUT)
    pi.set_mode(LEFT_IN1, pigpio.OUTPUT)
    pi.set_mode(LEFT_IN2, pigpio.OUTPUT)

    pi.set_PWM_frequency(RIGHT_IN1, 50)
    pi.set_PWM_range(RIGHT_IN1, 100)
    pi.set_PWM_frequency(RIGHT_IN2, 50)
    pi.set_PWM_range(RIGHT_IN2, 100)
    pi.set_PWM_frequency(LEFT_IN1, 50)
    pi.set_PWM_range(LEFT_IN1, 100)
    pi.set_PWM_frequency(LEFT_IN2, 50)
    pi.set_PWM_range(LEFT_IN2, 100)

# 　↓
def move_back(pi, speed):  #もとは前進
    print("後退         ↓")
    pi.set_PWM_dutycycle(RIGHT_IN1, speed)
    pi.write(RIGHT_IN2, 0)
    pi.write(LEFT_IN1, 0)
    pi.set_PWM_dutycycle(LEFT_IN2, speed)

# ↘
def move_back_R(pi, speed):
    print("右斜め後ろ   ↘")
    right_s = speed + DUTY_DIAGONAL
    left_s = speed - DUTY_DIAGONAL
    if right_s > MAX_SPEED:
        right_s = MAX_SPEED
    if left_s < MIN_SPEED:
        left_s = MIN_SPEED
    pi.set_PWM_dutycycle(RIGHT_IN1, right_s)
    pi.write(RIGHT_IN2, 0)
    pi.write(LEFT_IN1, 0)
    pi.set_PWM_dutycycle(LEFT_IN2, left_s)

# ↙
def move_back_L(pi, speed):
    print("左斜め後ろ   ↙")
    right_s = speed - DUTY_DIAGONAL
    left_s = speed + DUTY_DIAGONAL
    if right_s < MIN_SPEED:
        right_s = MIN_SPEED
    if left_s > MAX_SPEED:
        left_s = MAX_SPEED
    pi.set_PWM_dutycycle(RIGHT_IN1, right_s)
    pi.write(RIGHT_IN2, 0)
    pi.write(LEFT_IN1, 0)
    pi.set_PWM_dutycycle(LEFT_IN2, left_s)

# ↓
def move_forward(pi, speed): #もとは後退
    print("前進         ↓")
    left_s = speed + DUTY_CV
    if left_s > MAX_SPEED:
        left_s = MAX_SPEED
    pi.write(RIGHT_IN1, 0)
    pi.set_PWM_dutycycle(RIGHT_IN2, speed)
    pi.set_PWM_dutycycle(LEFT_IN1, speed)
    pi.write(LEFT_IN2, 0)

# ↗
def move_forward_R(pi, speed):
    print("右斜め前     ↗")
    right_s = speed + DUTY_DIAGONAL
    left_s = speed - DUTY_DIAGONAL
    if right_s > MAX_SPEED:
        right_s = MAX_SPEED
    if left_s < MIN_SPEED:
        left_s = MIN_SPEED
    pi.write(RIGHT_IN1, 0)
    pi.set_PWM_dutycycle(RIGHT_IN2, right_s)
    pi.set_PWM_dutycycle(LEFT_IN1, left_s)
    pi.write(LEFT_IN2, 0)

# ↖
def move_forward_L(pi, speed):
    print("左斜め前     ↖")
    right_s = speed - DUTY_DIAGONAL
    left_s = speed + DUTY_DIAGONAL
    if right_s < MIN_SPEED:
        right_s = MIN_SPEED
    if left_s > MAX_SPEED:
        left_s = MAX_SPEED
    pi.write(RIGHT_IN1, 0)
    pi.set_PWM_dutycycle(RIGHT_IN2, right_s)
    pi.set_PWM_dutycycle(LEFT_IN1, left_s)
    pi.write(LEFT_IN2, 0)

# ←
def move_right(pi, speed): #もとは左旋回
    print("右旋回       ←")
    left_s = speed + DUTY_CV
    if left_s > MAX_SPEED:
        left_s = MAX_SPEED
    pi.write(RIGHT_IN1, 0)
    pi.set_PWM_dutycycle(RIGHT_IN2, speed)
    pi.write(LEFT_IN1, 0)
    pi.set_PWM_dutycycle(LEFT_IN2, speed)

# →
def move_left(pi, speed): #もとは右旋回
    print("左旋回       →")
    left_s = speed + DUTY_CV
    if left_s > MAX_SPEED:
        left_s = MAX_SPEED
    pi.set_PWM_dutycycle(RIGHT_IN1, speed)
    pi.write(RIGHT_IN2, 0)
    pi.set_PWM_dutycycle(LEFT_IN1, speed)
    pi.write(LEFT_IN2, 0)

# 停止
def move_stop(pi):
    print("停止")
    pi.write(RIGHT_IN1, 0)
    pi.write(RIGHT_IN2, 0)
    pi.write(LEFT_IN1, 0)
    pi.write(LEFT_IN2, 0)

if __name__ == "__main__":
    pi = pigpio.pi()
    init_mortor(pi)

    speed = low_speed

    while True:
        move_stop(pi)
        sleep(2)
        move_forward(pi, speed)
        sleep(2)
        move_stop(pi)
        sleep(0.5)
        move_forward_R(pi, speed)
        sleep(2)
        move_stop(pi)
        sleep(0.5)
        move_forward_L(pi, speed)
        sleep(2)
        move_back(pi, speed)
        sleep(2)
        move_stop(pi)
        sleep(0.5)
        move_back_R(pi, speed)
        sleep(2)
        move_stop(pi)
        sleep(0.5)
        move_back_L(pi, speed)
        sleep(2)
        move_left(pi, speed)
        sleep(2)
        move_right(pi, speed)
        sleep(2)
        move_stop(pi)
        sleep(2)
