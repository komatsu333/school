#　じゃんけん課題
import socket
import sys

IPADDR = ""
PORT = 55555
PORT2 = 55655

argc = len(sys.argv)

def sockcv_setup(): #受信サーバーの立ち上げ
	sock_sv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock_sv.bind((IPADDR,PORT2))
	sock_sv.listen()
	sock_cl,addr = sock_sv.accept()
	client_ip = addr[0]
	client_port = addr[1]
	return sock_sv ,sock_cl ,addr


def send_janken(sock): #送信関数
	while True:
		print("1:グー\n2:チョキ\n3:パー\n")
		data = input("1～3の数字で入力してください\n>")
		if data == "exit":
			break
		else:
			try:
				ret = sock.send(data.encode('utf-8'))
				client_choise = data
				return int(client_choise)
				break
			except ConnectionResetError:
				break



def recv_janken(sock_cl,addr): #受信関数
	while True:
		try:
			print('\nサーバー側の選択を待っています\n')
			data = sock_cl.recv(1024) #待機
			if data == b"":
				break

			server_choise = data.decode('utf-8')
			hand_str_recv = {1:"グー", 2:"チョキ", 3:"パー"}
			server_hand_recv = hand_str_recv[int(server_choise)]
			print(addr[0] + "-> " +server_hand_recv+"\n")
			return int(server_choise)
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
	return hand_str[c] ,hand_str[s] ,result_table[(c,s)]

def main():
	if argc < 2:
		IPADDR = input('接続先IPアドレス：')
	else:
		IPADDR = sys.argv[1]

	try:
		print(f'{IPADDR}に接続します')
		print('\nじゃんけん開始\n')
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((IPADDR,PORT))

	except socket.error as e:
		print("接続エラー")
		print(e)
		sys.exit()

	try:
		client_choise = send_janken(sock)
		sock_sv ,sock_cl ,addr = sockcv_setup()
		server_choise = recv_janken(sock_cl,addr)
		client_hand ,server_hand ,result = judge_winner(client_choise,server_choise)

		print("client : "+client_hand)
		print("server : "+server_hand)
		print("\n"+result+"\n")

		sock.shutdown(socket.SHUT_RDWR)
		sock.close()
		sock_sv.shutdown(socket.SHUT_RDWR)
		sock_sv.close()
		sock_cl.shutdown(socket.SHUT_RDWR)
		sock_cl.close()

	except KeyboardInterrupt:
		print('終了します')
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()
		sock_sv.shutdown(socket.SHUT_RDWR)
		sock_sv.close()
		sock_cl.shutdown(socket.SHUT_RDWR)
		sock_cl.close()

if __name__ == '__main__':
	main()
