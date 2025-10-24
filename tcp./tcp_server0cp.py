#　じゃんけん課題
import socket
import datetime

IPADDR = ""
PORT = 55555
PORT2 = 55655

#####
sock_sv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_sv.bind((IPADDR,PORT))
sock_sv.listen()
print('TCP Server Start!')
#####

def sock_setup(): #送信サーバーの立ち上げ
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((IPADDR,PORT2))
	return sock

def send_janken(sock): #送信関数
	while True:
		print("1:グー\n2:チョキ\n3:パー\n")
		data = input("1～3の数字で入力してください\n>")
		if data == "exit":
			break
		else:
			try:
				ret = sock.send(data.encode('utf-8'))
				server_choise = data
				return int(server_choise)
				break
			except ConnectionResetError:
				break
def recv_janken(sock_cl,addr): #受信関数
	while True:
		try:
			print('クライアント側の選択を待っています\n')
			data = sock_cl.recv(1024) #待機
			if data == b"":
				break
			client_choise = data.decode('utf-8')
			hand_str = {1:"グー", 2:"チョキ", 3:"パー"}
			client_hand_recv = hand_str[int(client_choise)]
#			print(addr[0] + "-> " +client_hand_recv+"\n")
			return int(client_choise)
			break
		except ConnectionResetError:
			break

def judge_winner(c,s):
	hand_str = {1:"グー", 2:"チョキ", 3:"パー"}

	result_table = {
		(1, 1): "draw", (1, 2): "win",  (1, 3): "lose",
		(2, 1): "lose", (2, 2): "draw", (2, 3): "win",
		(3, 1): "win",  (3, 2): "lose", (3, 3): "draw"
	}
	return hand_str[c] ,hand_str[s] ,result_table[(s,c)]

def main():
	try:
		sock_cl,addr = sock_sv.accept()
		client_ip = addr[0]
		client_port = addr[1]

		dt_now = datetime.datetime.now()
		dt_str = dt_now.strftime("%Y/%m/%d %H:%M:%S")

		print(f'({dt_str} {client_ip}:{client_port} から接続されました')
		print('\nじゃんけん開始\n')

		client_choise = recv_janken(sock_cl,addr)
		sock = sock_setup()
		server_choise = send_janken(sock)
		client_hand ,server_hand ,result = judge_winner(client_choise,server_choise)

		print("\n"+addr[0] + "-> " +client_hand+"\n")

		print("client : "+client_hand)
		print("server : "+server_hand)
		print("\n"+result+"\n")

		print("\n"+client_ip + "から切断されました\n")
		sock_sv.shutdown(socket.SHUT_RDWR)
		sock_sv.close()
		sock_cl.shutdown(socket.SHUT_RDWR)
		sock_cl.close()
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()


	except KeyboardInterrupt:
		print('終了します')
		sock_sv.shutdown(socket.SHUT_RDWR)
		sock_sv.close()

if __name__ == '__main__':
	main()
