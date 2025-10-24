import socket
import datetime

IPADDR = ""
PORT = 55556

#####
sock_sv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_sv.bind((IPADDR,PORT))
print('UDP Server Start!')
#####

try:
	while True:
		data,cl_addr = sock_sv.recvfrom(1024)
		dt_now = datetime.datetime.now()
		dt_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")
		print(cl_addr[0] + "-> " +data.decode("utf-8"))

except KeyboardInterrupt:
	print('終了します')
	sock_sv.close()
