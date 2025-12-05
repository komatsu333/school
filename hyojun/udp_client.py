#!/usr/bin/env python
import socket
import sys
import cv2
import numpy as np
import struct

#IPADDR = "192.168.200.1"
# IPADDR = "192.168.76.204"
IPADDR = "0.0.0.0"
PORT = 55555

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IPADDR, PORT)) #bind()の引数はタプル型

        if sock is None:
            print("サーバへの接続に失敗しました...")
            return -1
        print("受信開始")
        while True:
            # 親機から送信されたデータを受け取る
            data, sv_addr = rcv_camera(sock)
            # 相手が未送信だと b''（長さ 0）を返す
            if data == b'':
                continue
            frame = decode_camera(data)
            if frame is not None:
                # 画像を表示
                cv2.imshow('frame', frame)
                # キー入力を待機
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print("終了します")
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        # ソケットクローズ
        if 'sock' in locals():
            sock.close()


### 関数定義 ###

def rcv_camera(sock) -> np.uint8:
    # フレームデータのサイズを受信
    data, addr = sock.recvfrom(4)
    if data != b'':
        size = struct.unpack('!I', data)[0]
        print(f"受信予定サイズ: {size} bytes")

        # フレームデータを受信
        received_data = b''
        while len(received_data) < size:
            packet, _ = sock.recvfrom(size - len(received_data))
            if not packet:
                break
            received_data += packet

        print(f"実際に受信したサイズ: {len(received_data)} bytes")
        return received_data, addr
    else:
        print(f"サイズデータの受信に失敗: {len(data)} bytes")
        return b'', addr

def decode_camera(data):
    try:
        # 受信したデータをデコード
        frame_data = np.frombuffer(data, dtype=np.uint8)
        # データを画像に変換
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"画像デコードエラー: {e}")
        return None

if __name__ == '__main__':
    main()
