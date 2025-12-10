#!/usr/bin/env python
import socket
import datetime
import cv2
import struct
import time
import threading
import serial
import sys
import pigpio
import os
import RPi.GPIO as GPIO

#プログラム
import servo
import mortors

midle_angle = 70    #サーボ中央(初期値)
angle = midle_angle #サーボ中央(初期値)
low_speed = 14      #低速
high_speed = 15     #高速
speed = low_speed   #速度の初期設定

stop_pin = 17       #仮ピン #非常停止ボタンが押されたのを検知
GPIO.setmode(GPIO.BCM)
GPIO.setup(stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pi = pigpio.pi()
if not pi.connected:
    print("pigpioに接続できませんでした")

IPADDR = ""
PORT1 = 55555
PORT2 = 55556   #予備

#サーボモータの初期位置
def init_servo():
    global angle, pi
    servo.servo_angle(pi, angle, 0.5) #サーボを初期位置に調整
    print("サーボモータ初期位置設定完了")

#モーターの初期設定
def init_mortor():
    global pi
    mortors.init_mortor(pi) #モーターの初期設定
    print("モーター初期設定完了")

# Xbeeコード
def rcv_xbee():
    global pi, angle, speed
    ser = None
    try:
        init_servo()  #サーボの初期位置調整
        init_mortor() #モーターの初期設定

        ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)
        print("XBee受信開始")
        while True:
            if ser.in_waiting:
                result_byte = ser.readline()
                result = result_byte.decode('UTF-8')

                if result == "F\n":     #前進
                    print("↑")
                    mortors.move_forward(pi,speed)

                if result == "FR\n":    #右前
                    print("↗")
                    mortors.move_forward_R(pi,speed)

                if result == "R\n":     #右旋回
                    print("→")
                    mortors.move_right(pi,speed)

                if result == "BR\n":    #右後
                    print("↘")
                    mortors.move_back_R(pi,speed)

                if result == "B\n":     #後退
                    print("↓")
                    mortors.move_back(pi,speed)

                if result == "BL\n":    #左後
                    print("↙")
                    mortors.move_back_L(pi,speed)

                if result == "L\n":     #左旋回
                    print("←")
                    mortors.move_left(pi,speed)

                if result == "FL\n":    #右前
                    print("↖")
                    mortors.move_forward_L(pi,speed)

                if result == "ST\n":    #停止
                    print("STOP")
                    mortors.move_stop(pi)

                if result == "UP\n":    #サーボ上向き
                    print("△")
                    if angle < midle_angle + 40:
                        angle += 10
                        servo.servo_angle(pi, angle, 0.1)
                    print(f"angle = {angle}")

                if result == "DO\n":    #サーボ下向き
                    print("▽")
                    if angle > midle_angle - 40:
                        angle -= 10
                        servo.servo_angle(pi, angle, 0.1)
                    print(f"angle = {angle}")

                if result == "CH\n":
                    print("可変")
                    if speed == low_speed: #低速 -> 高速
                        speed = high_speed
                        print("High Mode")
                        print(f"speed = {speed}")
                    else:                  #高速 -> 低速
                        speed = low_speed
                        print("LOW Mode")
                        print(f"speed = {speed}")

                if result == "EX\n": #プログラム終了
                    print("終了")
                    os.system("/usr/bin/sudo /sbin/poweroff")

                print(f"受信データ : {result}")

    except Exception as e:
        print(f"[XBee] エラー: {e}")

    finally:
        if ser is not None:
                ser.close()

#カメラ映像を送信
def main_server():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("カメラの初期化に失敗しました")
        return -1
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while True:
        sock_cl = None

        try:
            ports = [PORT1, PORT2]
            sock_sv = create_server(ports)

            if sock_sv is None:
                print("すべてのポートでバインドに失敗しました")
                break

            sock_sv.listen()
            print("TCP Server Start!")

            sock_cl, addr = sock_sv.accept()
            client_ip = addr[0]
            client_port = addr[1]

            dt_now = datetime.datetime.now()
            dt_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")
            print(f"({dt_str}) {client_ip}:{client_port} から接続されました")

            while True:
                try:
                    ret, frame = cap.read()
                    if not ret:
                        print("フレームの取得に失敗しました")
                        break

                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
                    result, frame_data = cv2.imencode('.jpg', frame, encode_para                                                                                                                                                                                                                                             m)
                    if not result:
                        print("画像のエンコードに失敗しました")
                        continue

                    size = len(frame_data)
                    sock_cl.send(struct.pack('!I', size))
                    sock_cl.sendall(frame_data)
                    time.sleep(0.03)

                except (BrokenPipeError, ConnectionResetError, ConnectionAborted                                                                                                                                                                                                                                             Error) as e:
                    print(f"{client_ip}:{client_port} から切断されました: {e}")
                    break
                except Exception as e:
                    print(f"通信エラー: {e}")
                    break

        except KeyboardInterrupt:
            print("終了します")
            break
        except Exception as e:
            print(f"予期しないエラー: {e}")
            time.sleep(1)
        finally:
            if sock_cl:
                try:
                    sock_cl.close()
                except:
                    pass
            if sock_sv:
                try:
                    sock_sv.close()
                except:
                    pass

    if cap is not None:
        cap.release()
    print("サーバーを終了しました")

#非常停止ボタンが押されたのを検知してモーターをストップ
def signal_lost(channel): #channel = pinの番号がでる
    print("非常停止ボタンが押されたためモーターを停止しました")
    #mortors.move_stop(pi)  #現時点では実装されていないのでprintのみ表示

def main():
    # Xbeeスレッド起動
    xbee_thread = threading.Thread(target=rcv_xbee, daemon=True)
    xbee_thread.start()

    # サーバースレッド起動
    server_thread = threading.Thread(target=main_server, daemon=True)
    server_thread.start()

    # 非常停止ボタンが押されたのを検知
    GPIO.add_event_detect(stop_pin, GPIO.FALLING, callback=signal_lost, bounceti                                                                                                                                                                                                                                             me=200)

    try:
        while True:
            time.sleep(1)   #ループ

    except KeyboardInterrupt:
        print("終了します")


def create_server(ports) -> socket.socket:
    sock = None
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", port))
            print(f"使用ポート : {port}")
            break
        except Exception as e:
            print(f"ポート {port} でのバインドに失敗: {e}")
            if sock:
                sock.close()
            sock = None
            continue

    return sock


if __name__ == "__main__":
    main()
