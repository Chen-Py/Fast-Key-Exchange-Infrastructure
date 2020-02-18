from socket import *
from threading import Thread
from pvcdatabase import Database
from fkealgo import FKE
import secrets
import pyDes
alliv = 2001061920010907101
def encrypt(data, key, iv = alliv):
    iv = iv.to_bytes(8, 'big')
    key = key.to_bytes(24, 'big')
    data = data.encode()
    k = pyDes.triple_des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    res = k.encrypt(data)
    return res
    
def decrypt(data, key, iv = alliv):
    iv = iv.to_bytes(8, 'big')
    key = key.to_bytes(24, 'big')
    k = pyDes.triple_des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    res = k.decrypt(data)
    res = res.decode()
    return res

class ServerBase(Thread):
	def __init__(self, clisocket, ip):
		Thread.__init__(self)
		self.clisock = clisocket
		self.usname = None
		self.logged = False
		self.ip = ip
		self.bufsiz = 1024
		self.database = Database('Library')
		self.algo = FKE()

	def user(self, string):
		name, Private_Code = string[0:-1].split(': ')
		Private_Code = Private_Code[1:-1].split(', ')
		for i in range(0,3):
			Private_Code[i] = int(Private_Code[i])
		Private_Code = tuple(Private_Code)
		return name, Private_Code

	def SendError(self):
		try:
			self.clisock.send('Unsuccessful'.encode())
		except:
			print('SendError Error')
		pass
	def NewUser(self):
		try:
			msg = self.clisock.recv(self.bufsiz).decode()
			name, Private_Code = self.user(msg)
		except:
			self.SendError()
			return
		addres = self.database.add(name, Private_Code)
		if not addres:
			self.SendError()
		else:
			self.clisock.send('Creat Successfully'.encode())
		pass

	def LoginTest(self):
		self.logging = True
		try:
			self.usname = self.clisock.recv(self.bufsiz).decode()
		except ConnectionResetError:
			self.logging = False
			return
		if not self.database.has(self.usname):
			self.SendError()
			self.logging = False
			return
		user = self.database.user(self.usname)
		self.test = secrets.token_hex(24)
		self.test = int('0x' + self.test, 16)
		coc, csc, self.key = self.algo.Make_Communication_Code(user.Private_Code[0], user.Private_Code[1], user.Private_Code[2], self.test)
		msg = coc.to_bytes(24, 'big')
		self.clisock.send(msg)
		self.clisock.send(self.ip.encode())
		pass

	def LoginCheck(self):
		if not self.logging:
			self.clisock.recv(self.bufsiz)
			SendError()
			return
		try:
			ip = self.clisock.recv(self.bufsiz)
			ip = decrypt(ip, self.key)
		except:
			return False
		if ip == self.ip:
			self.logged = True
			self.database.dict[self.usname].bind(self.ip)
			self.clisock.send(encrypt('Sign In Successfully', self.key))
		else:
			self.SendError() 
		self.logging = False
		pass
 
	def ChangePassword(self):
		if not self.logged:
			self.clisock.recv(self.bufsiz)
			self.SendError()
			return
		msg = self.clisock.recv(self.bufsiz)
		msg = decrypt(msg, self.key)
		name, Private_Code = self.user(msg)
		print(name)
		print(Private_Code)
		if not self.database.modify(name, Private_Code, self.ip):
			self.SendError()
			return
		msg = encrypt('Change Successfully', self.key)
		self.clisock.send(msg)
		pass

	def DelUser(self):
		if not self.logged: 
			self.SendError()
			pass
		name = self.clisock.recv(self.bufsiz)
		name = decrypt(name, self.key)
		if self.database.delet(name, self.ip):
			msg = encrypt('Delete Successfully', self.key)
			self.clisock.send(msg)
			self.usname = None
			self.logged = False
			self.ip = None
			pass
		else:
			self.SendError()
			pass
		pass

	def AskUser(self):
		name = self.clisock.recv(self.bufsiz).decode()
		user = self.database.user(name)
		if user == None:
			res = 'Unsuccessful'
		else:
			res = user.string()
		self.clisock.send(res.encode())
		pass

	def Error(self, mark):
		msg = mark + 'is not an avaliable mark'
		self.clisock.send(msg.encode())

	def run(self):
		while True:
			try:
				mark = self.clisock.recv(self.bufsiz).decode()
			except:
				print('logout')
				if self.usname != None:
					self.database.dict[self.usname].loginip = None
				break
			else:
				try:
					if mark == 'NUS':
						self.NewUser()
					elif mark == 'AFT':
						self.LoginTest()
					elif mark == 'RTT':
						self.LoginCheck()
					elif mark == 'CPC':
						self.ChangePassword()
					elif mark == 'DUS':
						self.DelUser()
					elif mark == 'AUS':
						self.AskUser()
					else:
						self.Error(mark)
				except:
					print('logout')
					if self.usname != None:
						self.database.dict[self.usname].loginip = None
					break
		self.clisock.close()





def run(host = '172.17.0.16', port = 21567, bufsiz = 1024, lissiz = 5):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(lissiz)
	print('Waiting...')
	while True:
		try:
			clisock, addr = sock.accept()
			print('...receive from' + str(addr))
			SB = ServerBase(clisock, addr[0])
			SB.start()
		except:
			print('error')
			continue
	sock.close()

run()