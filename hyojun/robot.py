#一方的にカメラ映像を出力する
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
low_speed = 11      #低速
high_speed = 20     #高速
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


def rcv_tcp():
    global pi, angle, speed

    HOST = "192.168.200.1"
    PORT = 60000  #

    try:
        init_servo()
        init_mortor()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((HOST, PORT))
            server.listen(1)
#            print(f"TCPサーバー起動中... ポート {PORT} で待機")

            while True:
                conn, addr = server.accept()
                with conn:
                    print(f"受信")
                    data = conn.recv(1024)
                    if not data:
                        continue

                    result = data.decode('utf-8').strip()
                    print(f"受信データ : {result}")

                    if result == "F":
                        print("↑")
                        mortors.move_forward(pi, speed)
                    elif result == "FR":
                        print("↗")
                        mortors.move_forward_R(pi, speed)
                    elif result == "R":
                        print("→")
                        mortors.move_right(pi, speed)
                    elif result == "BR":
                        print("↘")
                        mortors.move_back_R(pi, speed)
                    elif result == "B":
                        print("↓")
                        mortors.move_back(pi, speed)
                    elif result == "BL":
                        print("↙")
                        mortors.move_back_L(pi, speed)
                    elif result == "L":
                        print("←")
                        mortors.move_left(pi, speed)
                    elif result == "FL":
                        print("↖")
                        mortors.move_forward_L(pi, speed)
                    elif result == "ST":
                        print("STOP")
                        mortors.move_stop(pi)
                    elif result == "UP":
                        print("△")
                        if angle < midle_angle + 40:
                            angle += 10
                            servo.servo_angle(pi, angle, 0.1)
                        print(f"angle = {angle}")
                    elif result == "DO":
                        print("▽")
                        if angle > midle_angle - 40:
                            angle -= 10
                            servo.servo_angle(pi, angle, 0.1)
                        print(f"angle = {angle}")
                    elif result == "CH":
                        print("可変")
                        if speed == low_speed:
                            speed = high_speed
                            print("High Mode")
                        else:
                            speed = low_speed
                            print("LOW Mode")
                        print(f"speed = {speed}")
                    elif result == "EX":
                        print("終了")
                        os.system("/usr/bin/sudo /sbin/poweroff")

    except Exception as e:
        print(f"[TCP] エラー: {e}")

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

    sock_sv = create_server([PORT1, PORT2])
    if sock_sv is None:
        print("すべてのポートでバインドが失敗")
        cap.release()
        return

    client_addr = ("192.168.200.200", 55555)
    print("a")

    try:
        if sock_sv.fileno() == -1:
            print("ソケットが閉じられています")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("フレームの取得に失敗")
                break

            encode_pram = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
            result, frame_data = cv2.imencode('.jpg', frame, encode_pram)
            if not result:
                print("画像のエンコード失敗")
                continue

            size = len(frame_data)
            try:
                sock_sv.sendto(struct.pack('!I', size), client_addr)
                sock_sv.sendto(frame_data.tobytes(), client_addr)
                time.sleep(0.03)
            except Exception as e:
                print(f"送信エラー : {e}")
                break

    except KeyboardInterrupt:
        print("終了します")

    finally:
        if cap:
            cap.release()
        if sock_sv:
            try:
                sock_sv.close()
            except Exception as e:
                print(f"ソケットクローズ時のエラー: {e}")
        print("サーバー終了")



#非常停止ボタンが押されたのを検知してモーターをストップ
def signal_lost(channel): #channel = pinの番号がでる
    print("非常停止ボタンが押されたためモーターを停止しました")
    #mortors.move_stop(pi)  #現時点では実装されていないのでprintのみ表示

def main():
    # Xbeeスレッド起動
    tcp_thread = threading.Thread(target=rcv_tcp, daemon=True)
    tcp_thread.start()

    # サーバースレッド起動
    server_thread = threading.Thread(target=main_server, daemon=True)
    server_thread.start()

    # 非常停止ボタンが押されたのを検知
    GPIO.add_event_detect(stop_pin, GPIO.FALLING, callback=signal_lost, bouncetime=200)

    try:
        while True:
            time.sleep(1)   #ループ

    except KeyboardInterrupt:
        print("終了します")


def create_server(ports) -> socket.socket:
    sock = None
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
