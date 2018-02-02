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
        elif ((i + 4) < size2 and game[i] != 'X' and game[i+4] != 'X'): #vertical stick
            return True
    return False

def main():
    print('--------------------------------------')
    global game
    game = list(range(1,size2+1))

    n = 0

    while (checkPossible()):
        printboard()
        if n==1:
            n = 2
        else:
            n = 1
        raw = input('Player '+ str(n) +', Enter your next move "x,y": ')
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
                        game[x-1]='X'
                        game[y-1]='X'
                        break
                else:
                    raw = input('Unallowed move, please re-enter: ')
            except ValueError:
                raw = input('Invalid input, please re-enter in this format "x,y": ')
    printboard()
    print('--------------------------------------')
    print('Player',n,"is the winner!!! Congrats!!! :D")

size = 4
size2 = size*size

x = 'y'
game = []

print("""Two squares game:\n\tThis game is played on a board of 4 x 4 squares. Two players take turns;
each of them takes turn to place a rectangle (that covers two squares) on the board, covering
any 2 squares. Only one rectangle can be on a square. A square cannot be covered twice. The
last player who can place a card on the board is the winner. By megadardery :D:""")
print()
while x=='y':
    main()
    x = input('Play again? "y/n": ')
