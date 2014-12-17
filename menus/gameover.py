#======================================================================#
#
# Team:  
#    Hunter Quant
#    Edward Pryor
#    Nick Marasco
#    Shane Peterson
#    Brandon Williams
#    Jeremy Rose
#
# Last modification: 12/2/14 By: Shayne
#
# Description: Menu that comes up when you die.
#
#======================================================================#

#Our class imports
from player import Player

#Panda3d imports
from direct.gui.DirectGui import *

#game over menu
def init(n):
    
    #Switches between 2 game over images
    if n == 1:
        frame = DirectFrame(frameSize=(-1,-1,1,1), pos=(0,0,0))
        base.gameOverImage.setImage("./resources/gameOver1.png")
    else:
        frame = DirectFrame(frameSize=(-1,-1,1,1), pos=(0,0,0))
        base.gameOverImage.setImage("./resources/gameOver2.png")
    
    mainMenu = DirectButton(frame,text=("Main Menu","Main Menu","Main Menu","Main Menu"),scale=.1,command=startMain,pressEffect=1,pos=(0,0,-.4))
    replay = DirectButton(frame,text=("Restart Level","Restart Level","Restart Level","Restart Level"),scale=.1,command=reLevel,pressEffect=1,pos=(0,0,.1))
    
    base.taskMgr.remove("Spawn enemies")
    
    return frame
    
#Calls the main menu
def startMain():
    
    base.gameOverImage.hide()
    base.fsm.request('MainMenu', 1)

#Restarts the current level
def reLevel():
    
    base.player.show()
    base.player.resetEnergy()
    base.gameOverImage.hide()
    base.levelChanger.resetEnemy()
    base.fsm.request('Play', False)
    
