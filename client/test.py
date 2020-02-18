from clientbase import ClientBase
cpy = ClientBase()
print(cpy.clisock.state)
print(cpy.NewUser('Chen_Py', '123'))
print(cpy.NewUser('CPY', '456'))

while True:
	a = str(input('name >>> '))
	if(a == 'exit'):
		break
	b = str(input('password >>> '))
	if cpy.UserSignIn(a, b):
		print('True')
		break
	print('False')
cpy.DeletUser()
d = str(input('ask name >>>'))
print(cpy.AskForPoc(d))
cpy.clisock.close()
