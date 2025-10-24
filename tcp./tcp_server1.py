import socket
import datetime

IPADDR = ""
PORT = 55555

#####
sock_sv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_sv.bind((IPADDR,PORT))
sock_sv.listen()
print('TCP Server Start!')
#####

try:
	sock_cl,addr = sock_sv.accept()
	client_ip = addr[0]
	client_port = addr[1]

	dt_now = datetime.datetime.now()
	dt_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")

	print(f'({dt_str} {client_ip}:{client_port} から接続されました')


	while True:
		try:
			data = sock_cl.recv(1024)
			if data == b"":
				break
			print(addr[0] + "-> " +data.decode("utf-8"))
		except ConnectionResetError:
			break

	print(client_ip + "から切断されました")
	sock_sv.shutdown(socket.SHUT_RDWR)
	sock_sv.close()
	sock_cl.shutdown(socket.SHUT_RDWR)
	sock_cl.close()

except KeyboardInterrupt:
	print('終了します')
	sock_sv.shutdown(socket.SHUT_RDWR)
	sock_sv.close()
