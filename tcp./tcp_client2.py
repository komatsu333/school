import socket
import sys

IPADDR = ""
PORT = 55555

argc = len(sys.argv)
if argc < 2:
	IPADDR = input('接続先IPアドレス：')
else:
	IPADDR = sys.argv[1]

try:
	print(f'{IPADDR}に接続します')
	sock = socket.socket(socket.AF_INET)
	sock.connect((IPADDR,PORT))
except socket.error as e:
	print("接続エラー")
	print(e)
	sys.exit()

try:
	while True:
		data = input("> ")
		if data == "exit":
			break
		else:
			try:
				ret = sock.send(data.encode('utf-8'))
			except ConnectionResetError:
				break
except KeyboardInterrupt:
	print('終了します')

sock.shutdown(socket.SHUT_RDWR)
sock.close()
