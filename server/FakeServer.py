from socket import *

host = '192.168.31.162'
port = 21567
bufsiz = 1024
addr = (host, port)

sersock = socket(AF_INET, SOCK_STREAM)
sersock.bind(addr)
sersock.listen(5)

while True:
	print("Waiting...")
	clisock, addr = sersock.accept()
	print('...connected from : ' + str(addr))
	while True:
		try:
			mark = clisock.recv(bufsiz).decode()
			print(mark)
			msg = clisock.recv(bufsiz).decode()
			print(msg)
			clisock.send('Creat Successfully'.encode())
		except:
			print('Done')
			break