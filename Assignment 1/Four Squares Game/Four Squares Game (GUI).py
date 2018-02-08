import pygame, sys, random
from pygame.locals import *


FPS = 60 # frames per second setting
SURF = pygame.display.set_mode((550, 800))
FPSCLOCK = pygame.time.Clock()


CELLCOUNT = 4

pygame.init()

#ENUMS-------------------------------------
class gamestate:
    notstarted = 1
    running = 2
    stopped = 3

class colors:
    white       = (255, 255, 255)
    red         = (255, 0  , 0  )
    yellow      = (255, 255, 0  )
    lightyellow = (255, 230, 150)
    pink        = (255, 0  , 255)
    green       = (0  , 255, 0  )
    blue        = (0  , 0  , 255)
    black       = (0  , 0  , 0  )
    navyblue    = (60 , 60 , 100)

class cellstate:
    used = 1
    highlighted = 2
    normal = 3
#------------------------------------------
    
class Board:
            
    def __init__(self,count, screen,validity):
        self._cellcount = count
        self._cellcount2 = self._cellcount * self._cellcount
        self._bordersize = 3
        self._margin = 2
        self._cellsize = 60

        self._cellmargin = 4

        self.validityCheck = validity
        
        self.selected = [None, None]
        self.rectangles = []
        
        self.cells = [cellstate.normal] * self._cellcount2
        
        self.borderColor = colors.black

        self.cellColor = colors.white
        self.cellHighlightedColor = colors.lightyellow
        self.cellPlayer1Color = colors.red
        self.cellPlayer2Color = colors.blue
        
        self.setScreen(screen)

    def getMargin(self): return self._margin * self._drawconst
    def getBorderSize(self): return self._bordersize * self._drawconst
    def getCellSize(self): return self._cellsize * self._drawconst
    def getTotalSize(self): return self._totalsize * self._drawconst
    
    def setScreen(self,screen):
        self._totalsize = 2 * self._bordersize + self._margin*(self._cellcount - 1) + self._cellcount * self._cellsize
        self._drawconst = screen[2] / self._totalsize
        self._offsetx = screen[0]
        self._offsety = screen[1]

    def getCellAt(self,x,y):
        if self.getBoardBounds().collidepoint(x,y) == False: return
        for i in range(self._cellcount2):
            bounds = self.getBounds(i)
            if bounds.collidepoint(x, y):
                return i
        return None

    def getState(self, ind):
        return self.cells[ind]

    #returns True if the selection was successful
    def setSelected(self, ind, player):
        if self.getState(ind) == cellstate.used:
            self.selected = [None, None]
            return False
            
        if self.selected[0] is None:
            self.selected[0] = (ind,player)
            return False
        elif self.selected[1] is None:
            if (self.selected[0][0] == ind):
                self.selected = [None, None]
                return False
            self.selected[1] = (ind,player)
            a = self.selected[0][0]
            b = self.selected[1][0]
            if a > b: a,b = b,a
            
            self.selected = [None, None]
            
            if self.validityCheck(self,a,b):
                self.rectangles.append((a,b,player))
                self.cells[a]=cellstate.used
                self.cells[b]=cellstate.used
                return True
            else:
                return False
            
        else:
            raise Exception
            
    def setHighlighted(self,ind):
        for i in range(self._cellcount2):
            if self.cells[i] == cellstate.highlighted:
                self.cells[i] = cellstate.normal
        if ind==None: return
        elif self.cells[ind] == cellstate.normal:
            self.cells[ind] = cellstate.highlighted
        

    def getBounds(self, ind):
        x = self._offsetx + self.getBorderSize() + (self.getMargin() + self.getCellSize()) * (ind % self._cellcount)
        y = self._offsety + self.getBorderSize() + (self.getMargin() + self.getCellSize()) * (ind// self._cellcount)
        return pygame.Rect(x, y, self.getCellSize(), self.getCellSize())
    
    def getBoardBounds(self):
        return pygame.Rect(self._offsetx, self._offsety, self.getTotalSize(), self.getTotalSize())

    def draw(self,SURF):
        pygame.draw.rect(SURF, self.borderColor, self.getBoardBounds())
        for i in range(self._cellcount2):
            mycolor = self.cellColor
            if self.getState(i) == cellstate.highlighted:
                mycolor = self.cellHighlightedColor

            pygame.draw.rect(SURF, mycolor, self.getBounds(i))

        for i in self.selected:
            if (i is not None):
                myrect = self.getBounds(i[0])
                myrect.width-=self._cellmargin
                myrect.height-=self._cellmargin
                mycolor = self.cellPlayer1Color
                if i[1] == 2: mycolor = self.cellPlayer2Color
                pygame.draw.rect(SURF, mycolor, self.getBounds(i[0]),self._cellmargin)
                   
        for i in self.rectangles:
            x1,y1 = self.getBounds(i[0]).topleft
            x1 += self._cellmargin
            y1 += self._cellmargin
            x2,y2 = self.getBounds(i[1]).bottomright
            x2 -= self._cellmargin
            y2 -= self._cellmargin
            myrect = pygame.Rect(x1,y1,x2-x1,y2-y1)
            mycolor = self.cellPlayer1Color
            if i[2] == 2: mycolor = self.cellPlayer2Color
            pygame.draw.rect(SURF, mycolor, myrect)


def isvalid(self,a,b):
               
    if ((b-a == self._cellcount) or (b-a == 1 and (a+1) % self._cellcount != 0)):
        return True
    else:
        return False

def checkPossible(myBoard):
    for i in range(myBoard._cellcount2-1):
        if ((i+1) % myBoard._cellcount != 0 and (i+1)<myBoard._cellcount2 and myBoard.cells[i] != cellstate.used and myBoard.cells[i+1] != cellstate.used):             #horizontal stick
            return True
        elif ((i + myBoard._cellcount) < myBoard._cellcount2 and myBoard.cells[i] != cellstate.used and myBoard.cells[i+myBoard._cellcount] != cellstate.used):         #vertical stick
            return True
    return False
    
def getAImove(myBoard):
    assert myBoard._cellcount2 % 2 == 0
    a = myBoard._cellcount2 - myBoard.rectangles[-1][0] - 1
    b = myBoard._cellcount2 - myBoard.rectangles[-1][1] - 1
    return a,b

def getAIrandommove(myBoard):
    a = 0
    b = 0
    while True:
        shift1 = random.randint(0,myBoard._cellcount-2)
        shift2 = random.randint(0,myBoard._cellcount-1)
        vertical = bool(random.getrandbits(1))

        if (vertical):
            a = myBoard._cellcount * shift1 + shift2
            b = a + myBoard._cellcount
        else:
            a = shift1 + myBoard._cellcount * shift2
            b = a + 1
		
        if (myBoard.cells[a] != cellstate.used and myBoard.cells[b] != cellstate.used):
            break

    return a,b
    
def main():

    def newGame(ai):
        nonlocal AIplayer,player,myBoard,myGameState
        myBoard = Board(CELLCOUNT,(25,25,500,500),isvalid)
        myGameState = gamestate.running
        player = 1
        AIplayer = ai
    
    pygame.display.set_caption('Four squares game!')

    
    mousex = 0
    mousey = 0

    AIplayer = None
    player = None
    myBoard = None
    myGameState = None
    newGame(0)

    msgGameStateFont = pygame.font.Font('freesansbold.ttf', 30)
    msgGameOptionsFont = pygame.font.Font('freesansbold.ttf', 20)
    
    msgNewGame1 = msgGameOptionsFont.render("New Game (2 players)", True, colors.white, colors.black)
    msgNewGameRect1 = msgNewGame1.get_rect()
    msgNewGameRect1.topleft = (310, 680)

    msgNewGame2 = msgGameOptionsFont.render("New Game (vs. Easy AI)", True, colors.white, colors.black)
    msgNewGameRect2 = msgNewGame2.get_rect()
    msgNewGameRect2.topleft = (310, 710)

    msgNewGame3 = msgGameOptionsFont.render("New Game (vs. Hard AI)", True, colors.white, colors.black)
    msgNewGameRect3 = msgNewGame3.get_rect()
    msgNewGameRect3.topleft = (310, 740)

    msgsPrint = ((msgNewGame1,msgNewGameRect1), (msgNewGame2,msgNewGameRect2), (msgNewGame3,msgNewGameRect3))
    
    while True: # main game loop
        mouseclicked = False
        mymessage = "Player " + str(player) + " 's Turn"

        SURF.fill(colors.navyblue)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseclicked = True

        mycell = myBoard.getCellAt(mousex, mousey)

        if mouseclicked:
            if msgNewGameRect1.collidepoint(mousex, mousey):
                newGame(0)
                continue
            elif msgNewGameRect2.collidepoint(mousex, mousey):
                newGame(1)
                continue
            elif msgNewGameRect3.collidepoint(mousex, mousey):
                newGame(2)
                continue
            
            if myGameState == gamestate.running and mycell != None :
                if myBoard.setSelected(mycell,player) == True:
                    if checkPossible(myBoard) == False:
                        myGameState = gamestate.stopped
                    else:
                        if AIplayer == 1:
                            a,b = getAIrandommove(myBoard)
                            myBoard.setSelected(a,2)
                            myBoard.setSelected(b,2)
                            if checkPossible(myBoard) == False:
                                myGameState = gamestate.stopped
                                player = "AI"
                        elif AIplayer == 2:
                            a,b = getAImove(myBoard)
                            myBoard.setSelected(a,2)
                            myBoard.setSelected(b,2)
                            if checkPossible(myBoard) == False:
                                myGameState = gamestate.stopped
                                player = "AI"
                        else:
                            if player == 1:
                                player = 2
                            else:
                                player = 1

        else:
            if myGameState == gamestate.running:
                myBoard.setHighlighted(mycell)

        if myGameState == gamestate.running:
            mymessage = "Player " + str(player) + "'s Turn"
        else:
            if player == "AI":
                mymessage = "The AI has won :P Haha!"
            else:
                mymessage = "Player " + str(player) + " Won!!! Congratulations!!!"
        #drawing stuff        
        myBoard.draw(SURF)
        
        msgGameState = msgGameStateFont.render(mymessage, True, colors.white)
        msgGameStateRect = msgGameState.get_rect()
        msgGameStateRect.topleft = (25, 550)
        SURF.blit(msgGameState, msgGameStateRect)

        for i in msgsPrint:
            SURF.blit(i[0], i[1])
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
