class User:
	def __init__(self, name = None, Private_Code = None, IP = None):
		self.name = name
		self.Private_Code = Private_Code
		self.loginIP = IP
		pass

	def set(self, string):
		self.name, self.Private_Code = string[0:-1].split(': ')
		self.Private_Code = self.Private_Code[1:-1].split(', ')
		for i in range(0,3):
			self.Private_Code[i] = int(self.Private_Code[i])
		self.Private_Code = tuple(self.Private_Code)
		return self.name, self.Private_Code

	def info(self):
		return (self.name,self.Private_Code)

	def string(self):
		return self.name + ': ' + str(self.Private_Code) + '\n'

	def bind(self, IP):
		self.loginIP = IP
		pass

	def debind(self):
		liginIP = None
		pass


class Database:
	def __init__(self, name):
		self.name = name
		self.dict = {}
		try:
			self.file = open(name + '.txt', mode = 'r', encoding = 'utf-8')
		except FileNotFoundError:
			self.file = open(name + '.txt', mode = 'w', encoding = 'utf-8')
			self.file.close()
		else:
			self.lines = self.file.readlines()
			for line in self.lines:
				user = User()
				user.set(line)
				self.dict[user.name] = user
			del self.lines
			self.file.close()
		pass

	def add(self, name, Private_Code):
		if name in self.dict:
			return False
		self.file = open(self.name + '.txt', 'a', encoding = 'utf-8')
		user = User(name, Private_Code)
		self.dict[name] = user
		self.file.write(user.string())
		self.file.close()
		return True

	def updata(self):
		self.file = open(self.name + '.txt', 'w',encoding = 'utf-8')
		for name in self.dict:
			self.file.write(self.dict[name].string())
		self.file.close()

	def modify(self, name, Private_Code, IP):
		print(self.dict[name].loginIP != IP)
		if name not in self.dict or self.dict[name].loginIP != IP:
			return False
		print('Hello')
		user = User(name, Private_Code, IP)
		self.dict[name] = user
		self.updata()
		return True

	def delet(self, name, IP):
		if name in self.dict:
			if self.dict[name].loginIP != IP:
				return False
			del self.dict[name]
			self.updata()
			return True
		else: return False

	def has(self, name):
		if name in self.dict:
			return True
		else: return False

	def user(self, name):
		if name in self.dict:
			return self.dict[name]
		else: return None


