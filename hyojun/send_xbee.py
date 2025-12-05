import serial
import time

def send(code):
    try:
        ser = serial.Serial("/dev/ttyUSB0", 9600)
        ser.write(code.encode('utf_8'))
        print(f"Xbee送信 {repr(code)}")
        print(f"Send: {code}")
        time.sleep(0.2)
        ser.close()
    except Exception as e:
        print(f"Xbee送信エラー {e}")

if __name__ == '__main__':
    send("EX\n")
