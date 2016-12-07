from random import randint as rand
base=16
registers = {
	'R1' : rand(-(1<<(base-1)), (1<<(base-1))-1),
	'R2' : rand(-(1<<(base-1)), (1<<(base-1))-1),
	'R3' : rand(-(1<<(base-1)), (1<<(base-1))-1),
	'R4' : rand(-(1<<(base-1)), (1<<(base-1))-1),
}

additional = {
#overflow flag
	'OF' : 0,
#sign flag
	'SF' : 0,
#zero flag
	'ZF' : 0, 
#presentation flag
	'PF' : 0,
}

def tobinary(x):
	if (x>0):
		return ('0'*(base-len(bin(x).split('b')[1]))+bin(x).split('b')[1])
	else:
		rep = ''.join(map(str,[str(1-int(i)) for i in ('0'*(base-len(bin(abs(x)).split('b')[1]))+bin(abs(x)).split('b')[1]) ]))
		x = int(rep, 2)+1
		return ('0'*(base-len(bin(x).split('b')[1]))+bin(x).split('b')[1])



def out():
	for (x, y) in sorted(registers.items()):
		rep = tobinary(y)
		print("{0}: {2} {3} {4} {5} : [{1}]".format(x, y, rep[:4], rep[4:8],rep[8:12], rep[12:16]))
	print("OF = {0} SF = {1} ZF = {2} PF = {3}".format(additional['OF'], additional['SF'], additional['ZF'], additional['PF']))

#splitten array from input
def noMistakes(x):
	if x[0] not in ['add', 'load', 'mod']:
		return 'Not supported operation'
	if x[1] not in registers.keys():
		return '{0} is not an register'.format(x[1])
	if len(x)>3:
		return 'Processor supports only 2 params'
	return None


def makeOperation(x):
	if (x[0]=='load'):
		if (x[2] not in registers.keys()):
			registers[x[1]]=int(x[2])
		else:
			registers[x[1]]=int(registers[x[2]])
	elif (x[0]=='add'):
		if (x[2] not in registers.keys()):
			registers[x[1]]+=int(x[2])
		else:
			registers[x[1]]+=int(registers[x[2]])
	elif (x[0]=='mod'):
		if (x[2] not in registers.keys()):
			registers[x[1]]%=int(x[2])
		else:
			registers[x[1]]%=int(registers[x[2]])
	#Update additional information
	while registers[x[1]]>(1<<(base-1))-1:
		additional['OF']=1
		registers[x[1]]-=(1<<base)
	while registers[x[1]]<-((1<<(base-1))):
		additional['OF']=1
		registers[x[1]]+=(1<<base)
	s = tobinary(registers[x[1]])
	sm = sum(map(int, list(s[12:16])))
	if sm % 2==0:
		additional['PF']=1
	if registers[x[1]]==0:
		additional['ZF']=1
	if registers[x[1]]<0:
		additional['SF']=1



out()
while (1):
	additional['OF']=0
	additional['SF']=0
	additional['ZF']=0
	additional['PF']=0

	s=input('> ').split(' ')
	if (noMistakes(s)==None):
		try:
			makeOperation(s)
			out()
		except ZeroDivisionError:
			print('Division by 0')
	else:
		print(noMistakes(s))
