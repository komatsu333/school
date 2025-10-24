import socket
import threading
import datetime

IPADDR = ""
PORT = 55555



def recv_client(sock,addr):
	client_ip = addr[0]
	client_port = addr[1]

	dt_now = datetime.datetime.now()
	dt_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")
	print(f'({dt_str} {client_ip}:{client_port} から接続')

	while True:
		try:
			data = sock.recv(1024)
			if data == b"":
				break
			print(addr[0] + "->" + data.decode("utf-8"))
		except ConnectoinResetError:
			break
	print(client_ip + "から切断されました")
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()



def main():
	sock_sv = socket.socket(socket.AF_INET)
	sock_sv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock_sv.bind((IPADDR,PORT))
	sock_sv.listen()
	print('TCP Server Start!')
#####

	try:
		while True:
			sock_cl,addr = sock_sv.accept()
			dt_now = datetime.datetime.now()
			dt_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")

			print(f'({dt_str} {addr[0]} から接続されました')

			thread = threading.Thread(target = recv_client, args = (sock_cl,addr))
			thread.start()

	except KeyboardInterrupt:
		print('終了します')
		sock_sv.shutdown(socket.SHUT_RDWR)
		sock_sv.close()


if __name__ == '__main__':
	main()
