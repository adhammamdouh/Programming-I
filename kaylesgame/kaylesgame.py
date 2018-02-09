import random
import time
list5 = []
double = 0
element = 0
winning = 0
winning_hard = -50
list = []
double1 = []
numbers = ['1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9','0']
changer = 1
counter = 20
def printarr():
    for i in numbers:
        print(i , end = " ")
    print()
printarr()
while True:
    print("how do you want to play")
    print("enter 1 to two players")
    print("enter 2 to play with a robot")
    how_to_play = int(input())
    for k in range (0 , 200 , 1):
        if(changer == 1):
            print("player1 : " , end = "")
            maxx = input()
            if(len(maxx) == 2 or len(maxx) == 1):
                i = int(maxx)
                j = i
            else:
                i,j = maxx.split(",")
                i = int(i)
                j = int(j)
            changer = 2
        elif(how_to_play == 2 and changer == 2):
            print('computer :' )
            time.sleep(0.5)
            if (True):
                if(winning <= 50 ):
                    trick = 3
                elif(winning >= winning_hard):
                    trick = 2
                elif(winning_hard > winning):
                    trick = 4
            value = random.randint(0,1)
            for g in range (0,len(numbers)-1,1):
                if(numbers[g] != '-' and numbers[g+1] != '-'):
                    double += 1
                    double1.append(g)
                    double1.append(g+1)
                if(numbers[g] != '-'):
                    element += 1
                    list5.append(g+1)
            if(numbers[19] != '-'):
                element += 1
                list5.append(20)
            if((trick == 2 ) and element == 6 and double == 1):
                i = double1[0]
                j = double1[1]
                list5 = []
                double = 0
                element = 0
            elif(trick == 2 and (element == 4 and (double == 2 or double == 3)) or (element == 5)):
                i = random.choice(list5)
                j = 1
                maxx = chr(i)
                list5 = []
                double = 0
                element = 0
            elif(trick == 4 and element % 2 != 0):
                i = random.choice(list5)
                i = j
                maxx = chr(i)
                element = 0
            elif(value == 1):
                for t in range (0 , len(numbers)-1 , 1):
                    if(numbers[t] != '-' and numbers[t+1] != '-' and t != len(numbers)-1):
                        list.append(t+1)
                if(numbers[19] != '-' and numbers[18] != '-'):
                    list.append(19)
                if(list == []):
                    value = 0
                else :
                    i = random.choice(list)
                    list2 =[i+1]
                    j = random.choice(list2)
                    maxx = '111'
                list = []
            else :
                for t in range (0 , len(numbers) , 1):
                    if(numbers[t] != '-'):
                        list.append(t+1)
                i = random.choice(list)
                maxx = chr(i)
                j = i
                list = []
            changer = 1
        else:
            if(changer == 2):
                print("player2 : " , end = "")
                maxx = input()
                if(len(maxx) == 2 or len(maxx) == 1):
                    i = int(maxx)
                    j = i
                else:
                    i,j = maxx.split(",")
                    i = int(i)
                    j = int(j)
                changer = 1
        if(numbers[i-1] == '-' ):
            print(i , " was token before")
            if(changer == 2):
                changer = 1
            else:
                changer = 2
        elif(numbers[j-1] == '-' and (len(maxx) != 1 or len(maxx) != 2) ):
            print(j , " was token before")
            if(changer == 2):
                changer = 1
            else:
                changer = 2
        elif(i == j and (len(maxx) == 2 or len(maxx) == 1)):
            numbers[i - 1] = '-'
            printarr()
            counter -= 1
        elif((i != j+1) and (i != j-1) ):
            print("error the numbers are not adjacent")
            if(changer == 2):
                changer = 1
            else:
                changer = 2
        elif(i == j+1 or i == j-1):
            numbers[i-1] = '-'
            numbers[j-1] = '-'
            printarr()
            counter -= 2
        if(counter == 0):
            if(changer == 1 and how_to_play != 2):
                print("player2 is the winner")
            elif(changer == 2 ):
                print("player1 is the winner")
                winning += 10
                winning_hard += 20
            elif(changer == 1 and how_to_play == 2):
                print("the robot is the winner")
            print()
            break
        
