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

def getAImove(x,y):
    a = size2-x+1
    b = size2-y+1
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

def coregame(human):
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
            x,y = getAImove(x,y)
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
    x = input('Want to play againest a human, or againest world\'s best AI? "computer/human"')
    while (x=='human' or x=='computer'):
        if (x == 'human'):
            coregame(True)
        else:
            coregame(False)
        x = input('Play again? againest a human or againest AI? "computer/human": ')

size = 4        #For the AI to work properly, size should never be odd
size2 = size*size

game = []

main()
