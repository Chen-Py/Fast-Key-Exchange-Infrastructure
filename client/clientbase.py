from fkealgo import FKE
from hashlib import blake2b
import pyDes
from clientsocket import TcpCliSock

allm = 6277101735386680763835789423207666416102355444464034512659
alliv = 2001061920010907101
algo = FKE()


def get_hash(obj):
	myhash = blake2b(digest_size = 24)
	myhash.update(obj.encode('utf-8'))
	num = myhash.hexdigest()
	num = int('0x' + num, 16)
	return num

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

class ClientBase:
	def __init__(self):
		self.clisock = TcpCliSock()
		self.key = None
		self.name = None
		self.logged = False
		pass

	def userstr(self, name, password):
		Private_Code = algo.Make_Private_Code(get_hash(name), allm, get_hash(password))[0]
		return name + ': ' + str(Private_Code) + '\n'

	def NewUser(self, name, password):
		if self.clisock.state != 'Connected' or name == '' or password == '':
#			print('Unsuccessful')
			return False
		msg = self.userstr(name, password)
		try:
			self.clisock.send('NUS', msg)
			res = self.clisock.recvstr()
#			print(res)
		except:
			return False
		if(res != 'Creat Successfully'):
			return False
		return True

	def UserSignIn(self, name, password):
		if self.clisock.state != 'Connected' or name == '' or password == '':
#			print('Unsuccessful')
			return False
		try:
			self.clisock.send('AFT', name)
			msg = self.clisock.recvbyte()
			if(msg == b'Unsuccessful'):
#				print('Unsuccessful')
				return False
			Communication_Open_Code = int(123).from_bytes(msg, 'big')
			ip = self.clisock.recvstr()
			self.key = algo.Make_Key(Communication_Open_Code, allm, get_hash(password))
			msg = encrypt(ip, self.key)
			self.clisock.send('RTT', msg)
			res = self.clisock.recvbyte()
		except:
			return False
		if res == b'Unsuccessful':
#			print("Unsuccessful")
			return False
		if(decrypt(res, self.key) != 'Sign In Successfully'):
			return False
#		print(decrypt(res, self.key))
		self.name = name
		self.logged = True
		return True

	def ChangePassword(self, new_password):
		if self.clisock.state != 'Connected' or self.logged == False or new_password == '':
#			print("Unsuccessful")
			return False
		try:
			msg = self.userstr(self.name, new_password)
			msg = encrypt(msg, self.key)
			self.clisock.send('CPC', msg)
			res = self.clisock.recvbyte()
		except:
#			print('Unsuccessful')
			return False
		if res == b'Unsuccessful':
#			print('Unsuccessful')
			return False
		try: 
			if(decrypt(res, self.key) != 'Change Successfully'):
#				print("Unsuccessful ")
				return False
		except:
#			print('Unsuccessful')
			return False
#		print('Change Successfully')
		return True

	def DeletUser(self):
		if self.clisock.state != 'Connected' or self.logged == False:
#			print('Unsuccessful')
			return False
		try:
			msg = encrypt(self.name, self.key)
			self.clisock.send('DUS', msg)
			res = self.clisock.recvbyte()
			if res == b'Unsuccessful':
#				print('Unsuccessful')
				return False
		except:
#			print('Unsuccessful')
			return False
		if(decrypt(res, self.key) != 'Delete Successfully'):
			return False
#		print('Delete %s Successfully' %self.name)
		return True

	def AskForPoc(self, name):
		if self.clisock.state != 'Connected' or name == '':
#			print('Unsuccessful')
			return False
		try:
			self.clisock.send('AUS', name.encode())
			res = self.clisock.recvstr()
		except:
			return False
		if res == 'Unsuccessful':
			return False
		return res

