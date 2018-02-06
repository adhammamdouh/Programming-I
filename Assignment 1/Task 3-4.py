import random

def printboard():
	print()
	for i,x in enumerate(game):
		print(x, end="\t")
		if ((i+1) % size == 0): print()
	print()

def checkPossible():
	for i in range(size2):
		if ((i+1) % size != 0 and (i+1)<size2 and game[i] != 'X' and game[i+1] != 'X'): #horizontal stick
			return True
		elif ((i + size) < size2 and game[i] != 'X' and game[i+size] != 'X'): #vertical stick
			return True
	return False

def getAImove(x,y):
	a = size2-x+1
	b = size2-y+1
	print("Hmm.... I will do", a, ",", b)
	return a,b

def getAIrandommove():
	a = 0
	b = 0
	while True:
		shift1 = random.randint(0,size-2)
		shift2 = random.randint(0,size-1)
		vertical = bool(random.getrandbits(1))

		if (vertical):
			a = 1 + size * shift1 + shift2
			b = a + size
		else:
			a = shift1 + 1 + size * shift2
			b = a + 1
		if (game[a-1]!='X' and game[b-1]!='X'):
			break
	print("Hmm.... I will do", a, ",", b)
	return a,b

def getvalidmove(turn):
	raw = input('Player '+ turn +', Enter your next move "x,y": ')

	while True:
		try:
			x,y = raw.split(',')
			x = int(x)
			y = int(y)
			if (x > y): x,y = y,x

			if ((x > 0 and y > 0) and (x <= size2 and y <= size2) and ((y-x == size) or (y-x == 1 and x % size != 0))):
				if (game[x-1]=='X' or game[y-1]=='X'):
					raw = input('The square is covered, please re-enter: ')
				else:
					return x,y
			else:
				raw = input('Unallowed move, please re-enter: ')
		except ValueError:
			raw = input('Invalid input, please re-enter in this format "x,y": ')

def coregame(human,randomAI = False):
	print('--------------------------------------')
	global game
	game = list(range(1,size2+1))

	turn = "0"
	x = 0
	y = 0
	while (checkPossible()):
		printboard()
		if turn == "1":
			turn = "2"
		else:
			turn = "1"
		if (human==False and turn == "2"):
			if randomAI : x,y = getAIrandommove()
			else : x,y = getAImove(x,y)
		else:
			x,y = getvalidmove(turn)

		game[x-1]='X'
		game[y-1]='X'
	printboard()
	print('--------------------------------------')
	if (human==False and turn == "2"):
		print('Hahaha! I win. Nobody can beat Mr. perfect AI :D')
	else:
		print('Player',turn,"is the winner!!! Congrats!!! :D")


def main():
	print("""Two squares game:\n\tThis game is played on a board of 4 x 4 squares. Two players take turns;
each of them takes turn to place a rectangle (that covers two squares) on the board, covering
any 2 squares. Only one rectangle can be on a square. A square cannot be covered twice. The
last player who can place a card on the board is the winner. By megadardery :D:""")

	print()
	x = input('How many players are going to play? "1/2": ')
	while (x=="1" or x=="2"):
		if (x == "2"):
			coregame(True)
		else:
			while True:
				y = input('Choose the computer level "easy/hard": ')
				if y=="hard":
					y = False
					break
				elif y == "easy":
					y = True
					break
				else:
					print("Couldn't interpret your input.")


			coregame(False,y)
		x = input('Play again? How many players? "1/2": ')

size = 4		#For the AI to work properly, size should never be odd
size2 = size*size

mychoices = []
for i in range(1,size2-size):
	if (i%size!=0): mychoices.append(i)

game = []

main()
