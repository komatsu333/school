import serial

ser = serial.Serial("/dev/ttyS0", 9600, timeout = 0)

try:
        while True:
                if ser.in_waiting:
                        result_byte = ser.read(ser.in_waiting)
                        result = result_byte.decode('UTF-8')

                        if result == "F\n":
                            print("↑")

                        if result == "FR\n":
                            print("↗")

                        if result == "R\n":
                            print("→")

                        if result == "BR\n":
                            print("↘")

                        if result == "B\n":
                            print("↓")

                        if result == "BL\n":
                            print("↙")

                        if result == "L\n":
                            print("←")

                        if result == "FL\n":
                            print("↖")

                        if result == "UP\n":
                            print("△")

                        if result == "DO\n":
                            print("▽")

                        if result == "CH\n":
                            print("可変")

                        if result == "EX\n":
                            print("終了")

                        print(f"受信データ : {result}")
except:
        print("exit")
        ser.close()
