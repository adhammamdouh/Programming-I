import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

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
        
class Board:
            
    def __init__(self,screen,validity):
        self._cellcount = 4
        self._cellcount2 = self._cellcount * self._cellcount
        self._bordersize = 3
        self._margin = 2
        self._cellsize = 60

        self._cellmargin = 4

        self.validityCheck = validity
        
        self.selected = [None, None]
        self.rectangles = []
        
        self.cells = [cellstate.normal] * self._cellcount2
        
        self.marginColor = colors.blue
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

    def draw(self):
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

def checkPossible():
    for i in range(myBoard._cellcount2-1):
        if ((i+1) % myBoard._cellcount != 0 and (i+1)<myBoard._cellcount2 and myBoard.cells[i] != cellstate.used and myBoard.cells[i+1] != cellstate.used):             #horizontal stick
            return True
        elif ((i + myBoard._cellcount) < myBoard._cellcount2 and myBoard.cells[i] != cellstate.used and myBoard.cells[i+myBoard._cellcount] != cellstate.used):         #vertical stick
            return True
    return False
    

def main():
    global myBoard
    pygame.display.set_caption('Four squares game!')
    
    mousex = 0
    mousey = 0

    
    myBoard = Board((25,25,500,500),isvalid)
    myGameState = gamestate.running
    player = 1

    msgNewGame = msgGameOptionsFont.render("New Game", True, colors.white, colors.black)
    msgNewGameRect = msgNewGame.get_rect()
    msgNewGameRect.topleft = (380, 680)

    print(player)
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
            if msgNewGameRect.collidepoint(mousex, mousey):
                myBoard = Board((25,25,500,500),isvalid)
                myGameState = gamestate.running
                player = 1
                continue
                
            if myGameState == gamestate.running and mycell != None :
                if myBoard.setSelected(mycell,player) == True:
                    if checkPossible() == False:
                        myGameState = gamestate.stopped
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

            mymessage = "Player " + str(player) + " Won!!! Congratulations!!!"
        #drawing stuff        
        myBoard.draw()
        
        msgGameState = msgGameStateFont.render(mymessage, True, colors.white)
        msgGameStateRect = msgGameState.get_rect()
        msgGameStateRect.topleft = (25, 550)
        SURF.blit(msgGameState, msgGameStateRect)

        SURF.blit(msgNewGame, msgNewGameRect)
        
        pygame.display.update()
        fpsClock.tick(FPS)


myBoard = None
SURF = pygame.display.set_mode((550, 800))

msgGameStateFont = pygame.font.Font('freesansbold.ttf', 30)
msgGameOptionsFont = pygame.font.Font('freesansbold.ttf', 25)

class gamestate:
    notstarted = 1
    running = 2
    stopped = 3

if __name__ == '__main__':
    main()
