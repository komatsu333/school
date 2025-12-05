#サーバーからの動画をsaveボタンを押すと表示
#結合テスト - 同期回復機能付きバッファ管理
#tcp -> udp
#Xbee -> tcp
import tkinter as tk
import tkinter.filedialog
import udp_client
from PIL import Image, ImageTk
import cv2
import send_tcp
import os
import struct
import datetime
import socket
import time

#ボタンのレイアウト
x1 = 10
x2 = 85
x3 = 160
y1 = 100 + 40
y2 = 175 + 40
y3 = 250 + 40
btn_w = 5       #矢印ボタンの横
btn_h = 10       #矢印ボタンの縦
btn_low = 380   #openボタンなどの高さ
btn_x = 680 + 20     #右側ボタンのx座標
screen_w = 440  #カメラ映像のサイズ
screen_h = 360  #
speed_y = 10 + 20
font_size = 13
btm_w = 3
btn_h = 2

btn_delay = 100
btn_interval = 500

global_frame = None
last_valid_frame = None  # バッファクリア時の最後の有効フレーム
show_mode = False  # False: カメラ表示, True: 画像表示
consecutive_errors = 0  # 連続エラーカウント

status = "low" #現在のスピード　(low or high)




def recv_exact(sock, size, blocking=True):
        """指定バイト数を確実に受信する"""
        data = b''
        sock.setblocking(blocking)

        try:
                while len(data) < size:
                        chunk = sock.recv(size - len(data))
                        if not chunk:
                                return None
                        data += chunk
                return data
        except socket.error:
                return None

def reset_socket_sync(sock):
        """ソケットの同期をリセット"""
        print("ソケット同期をリセットします...")
        try:
                sock.setblocking(False)
                # バッファを完全にクリア
                discarded = 0
                while True:
                        try:
                                chunk = sock.recv(65536)
                                if not chunk:
                                        break
                                discarded += len(chunk)
                        except socket.error:
                                break

                if discarded > 0:
                        print(f"{discarded} バイトを破棄しました")

                # 少し待機して新しいフレームを待つ
                time.sleep(0.1)

        except Exception as e:
                print(f"同期リセットエラー: {e}")
        finally:
                sock.setblocking(True)

def get_latest_frame_safe(sock):
        """
        安全にバッファから最新フレームを取得
        同期エラー時は自動回復
        """
        global last_valid_frame, consecutive_errors

        # ブロッキングモードで1フレームだけ取得（シンプルな方式）
        try:
                sock.setblocking(True)
                sock.settimeout(1.0)  # 1秒タイムアウト

                # サイズヘッダーを確実に4バイト読む
                size_data = recv_exact(sock, 4, blocking=True)
                if size_data is None or len(size_data) != 4:
                        consecutive_errors += 1
                        if consecutive_errors >= 3:
                                reset_socket_sync(sock)
                                consecutive_errors = 0
                        return last_valid_frame

                size = struct.unpack('!I', size_data)[0]

                # サイズの妥当性チェック（JPEGフレームの想定サイズ）
                if size < 100 or size > 100000:  # 100バイト〜100KB
                        print(f"異常なサイズ検出: {size} バイト、同期リセットします")
                        reset_socket_sync(sock)
                        consecutive_errors = 0
                        return last_valid_frame

                # データ本体を確実に受信
                frame_data = recv_exact(sock, size, blocking=True)
                if frame_data is None or len(frame_data) != size:
                        consecutive_errors += 1
                        if consecutive_errors >= 3:
                                reset_socket_sync(sock)
                                consecutive_errors = 0
                        return last_valid_frame

                # デコード試行
                frame = udp_client.decode_camera(frame_data)
                if frame is None:
                        consecutive_errors += 1
                        if consecutive_errors >= 3:
                                print("デコード失敗が続いています、同期リセットします")
                                reset_socket_sync(sock)
                                consecutive_errors = 0
                        return last_valid_frame

                # 成功
                consecutive_errors = 0
                last_valid_frame = frame
                return frame

        except socket.timeout:
                print("フレーム受信タイムアウト")
                consecutive_errors += 1
                if consecutive_errors >= 5:
                        reset_socket_sync(sock)
                        consecutive_errors = 0
                return last_valid_frame

        except Exception as e:
                print(f"フレーム取得エラー: {e}")
                consecutive_errors += 1
                if consecutive_errors >= 3:
                        reset_socket_sync(sock)
                        consecutive_errors = 0
                return last_valid_frame
        finally:
                try:
                        sock.settimeout(None)
                except:
                        pass

def skip_old_frames(sock, max_skip=10):
        """
        古いフレームをスキップして最新フレームに近づく
        ただし、同期を崩さないように慎重に
        """
        global last_valid_frame

        skipped = 0
        sock.setblocking(False)

        try:
                for _ in range(max_skip):
                        try:
                                # サイズヘッダー確認
                                size_data = sock.recv(4, socket.MSG_PEEK)  # PEEKで覗き見
                                if len(size_data) < 4:
                                        break

                                size = struct.unpack('!I', size_data)[0]

                                # サイズチェック
                                if size < 100 or size > 100000:
                                        break

                                # 実際に読み捨て
                                sock.recv(4)  # サイズヘッダー
                                sock.recv(size)  # データ本体
                                skipped += 1

                        except socket.error:
                                break

                if skipped > 0:
                        print(f"{skipped} フレームをスキップしました")

        except Exception as e:
                print(f"スキップ中エラー: {e}")
        finally:
                sock.setblocking(True)

def capture_camera(sock, video_label):
        global global_frame, show_mode

        # Showモード中はカメラ更新をスキップ
        if show_mode:
                root.after(30, lambda: capture_camera(sock, video_label))
                return

        try:
                # 定期的に古いフレームをスキップ（5回に1回）
                if hasattr(capture_camera, 'call_count'):
                        capture_camera.call_count += 1
                else:
                        capture_camera.call_count = 0

                if capture_camera.call_count % 5 == 0:
                        skip_old_frames(sock, max_skip=3)

                # 最新フレームを取得
                frame = get_latest_frame_safe(sock)

                if frame is not None:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        #frame = cv2.resize(frame, (380, 230))
                        frame = cv2.resize(frame, (screen_w, screen_h))
                        global_frame = frame
                        img = Image.fromarray(frame)
                        imgtk = ImageTk.PhotoImage(image=img)
                        video_label.imgtk = imgtk
                        video_label.config(image=imgtk)

        except Exception as e:
                print(f"カメラキャプチャーエラー: {e}")
                root.after(100, lambda: capture_camera(sock, video_label))
                return

        root.after(30, lambda: capture_camera(sock, video_label))

def save_image():
        global global_frame
        if global_frame is not None:
                # ファイル名を生成（タイムスタンプを使用）
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                # imgディレクトリが存在しない場合は作成
                os.makedirs("./img", exist_ok=True)

                filename = f"./img/capture_{timestamp}.png"
                # RGB -> BGR に変換してから保存
                frame_bgr = cv2.cvtColor(global_frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(filename, frame_bgr)
                print(f"画像を保存しました: {filename}")
        else:
                print("not picture")

def open_image(video_label):
        global show_mode, global_frame

        # imgディレクトリが存在しない場合は作成
        os.makedirs("./img", exist_ok=True)

        # ファイル選択ダイアログ
        file_path = tk.filedialog.askopenfilename(
                title="画像ファイルを選択",
                initialdir="./img/",
                filetypes=[("Image File","*.png"), ("All Files","*.*")]
        )

        if file_path:
                # 選択された画像を読み込み
                image = cv2.imread(file_path)
                if image is not None:
                        # RGB変換とリサイズ
                        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        frame_resized = cv2.resize(frame_rgb, (screen_w, screen_h))

                        # 表示
                        img = Image.fromarray(frame_resized)
                        imgtk = ImageTk.PhotoImage(image=img)
                        video_label.imgtk = imgtk
                        video_label.config(image=imgtk)

                        # Showモードに切り替え
                        show_mode = True
                        print(f"画像を表示しました: {file_path}")
                else:
                        print("画像の読み込みに失敗しました")

def return_to_camera(sock):
        global show_mode, consecutive_errors

        # Cameraモードに切り替え
        show_mode = False
        consecutive_errors = 0
        print("カメラ表示に戻りました")

        # バッファをリセット
        reset_socket_sync(sock)

def ch_speed(speed_btn):
        global status
        if status  == "low":    #低速 -> 高速
                status = "high"
                print(f"speed = {status}")
        else:                   #高速 -> 低速
                status = "low"
                print(f"speed = {status}")

        speed_btn.config(text = f"現在：{status}")

def init_gui():
        global status

        #screen
        screen_frame = tk.Frame(root, width=screen_w, height=screen_h, bg="white", relief="sunken", bd=2)
        screen_frame.place(x=x3+70, y=10)
        screen_label = tk.Label(screen_frame, text="screen", bg="white")
        screen_label.place(relx=0.5, rely=0.5, anchor="center")
        video_label = tk.Label(screen_frame)
        video_label.pack()

        # UDP接続を非同期で開始
        print("UDP接続を開始します...")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #server_address = ("192.168.200.1", 55555)
        sock.bind(("0.0.0.0", 55555))

        frame_picture = capture_camera(sock, video_label)

        #speed_btn
        speed_btn = tk.Button(root, text=f"現在：{status}", width=6, height=3, highlightthickness=0, command=lambda: (send_tcp.send("CH\n"), ch_speed(speed_btn)), repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        speed_btn.place(x=x2-5, y=speed_y)

        #direction_btn
        f_btn  = tk.Button(root, text="↑", width=btn_w, height=btn_h, command=lambda: send_tcp.send("F\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, highlightthickness=0, background="white", activebackground="white")
        f_btn.place(x=x2, y=y1)

        fr_btn = tk.Button(root, text="↗", width=btn_w, height=btn_h, command=lambda: send_tcp.send("FR\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        fr_btn.place(x=x3, y=y1)

        r_btn  = tk.Button(root, text="→", width=btn_w, height=btn_h, command=lambda: send_tcp.send("R\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        r_btn.place(x=x3, y=y2)

        br_btn = tk.Button(root, text="↘", width=btn_w, height=btn_h, command=lambda: send_tcp.send("BR\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        br_btn.place(x=x3, y=y3)

        b_btn  = tk.Button(root, text="↓", width=btn_w, height=btn_h, command=lambda: send_tcp.send("B\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        b_btn.place(x=x2, y=y3)

        bl_btn = tk.Button(root, text="↙", width=btn_w, height=btn_h, command=lambda: send_tcp.send("BL\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        bl_btn.place(x=x1, y=y3)

        l_btn  = tk.Button(root, text="←", width=btn_w, height=btn_h, command=lambda: send_tcp.send("L\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        l_btn.place(x=x1, y=y2)

        fl_btn = tk.Button(root, text="↖", width=btn_w, height=btn_h, command=lambda: send_tcp.send("FL\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        fl_btn.place(x=x1, y=y1)

        #stop_btn - stop
        st_btn = tk.Button(root, text="STOP", width=btn_w, height=btn_h, command=lambda: send_tcp.send("ST\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        st_btn.place(x=x2, y=y2)

        #open_btn - 保存画像を開く
        open_btn = tk.Button(root, text="open", width=6, height=4, command = lambda: open_image(video_label),
                            background="white", activebackground="white")
        open_btn.place(x=250, y=btn_low)

        #save_btn - 現在の画像を保存
        save_btn = tk.Button(root, text="save", width=6, height=4, command = lambda: save_image(),
                            background="white", activebackground="white")
        save_btn.place(x=390, y=btn_low)

        #camera_btn - カメラ表示に戻る
        camera_btn = tk.Button(root, text="camera", width=6, height=4, command = lambda: return_to_camera(sock),
                            background="white", activebackground="white")
        camera_btn.place(x=530, y=btn_low)

        #servo_btn
        up_btn = tk.Button(root, text="△", width=5, height=2, command=lambda: send_tcp.send("UP\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        up_btn.place(x=btn_x, y=y2)

        down_btn = tk.Button(root, text="▽", width=5, height=2, command=lambda: send_tcp.send("DO\n"),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        down_btn.place(x=btn_x, y=y3)

        #exit_btn
        #exit_btn = tk.Button(root, text="exit", width=5, height=3, command=lambda: (send_tcp.send("EX\n"), os.system("/usr/bin/sudo /sbin/poweroff")),
        #                    repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")

        exit_btn = tk.Button(root, text="exit", width=5, height=3, command=lambda: root.quit(),
                            repeatdelay=btn_delay, repeatinterval=btn_interval, background="white", activebackground="white")
        exit_btn.place(x=btn_x, y=25)

        #main loop start
        root.mainloop()

#mainwindow
root = tk.Tk()
root.title("GUI")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#root.geometry(f"{screen_width}x{screen_height}") #本番はこれをコメント化して　↓を実行
root.attributes('-fullscreen',True) #全画面　Exitが電源を切るのでいったんコメント化中
root.configure(bg="lightgray")

if __name__ == '__main__':
        init_gui()
