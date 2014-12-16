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

from direct.gui.DirectGui import *

def init(n):
    
    if n == 1:
        frame = DirectFrame(frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0), image="resources/gameOver1.png")
    else:
        frame = DirectFrame(frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0), image="resources/gameOver2.png")
    
    mainMenu = DirectButton(frame,text=("Main Menu","Main Menu","Main Menu","Main Menu"),scale=.1,command=startMain,pressEffect=1,pos=(-.5,0,-.5))
    replay = DirectButton(frame,text=("Restart Level","Restart Level","Restart Level","Restart Level"),scale=.1,command=reLevel,pressEffect=1,pos=(.5,0,-.5))
    
    base.taskMgr.remove("Spawn enemies")
    
    return frame
    
def startMain():
    base.fsm.request('MainMenu', 1)
    
def reLevel():
    base.levelChanger.resetEnemy()
    base.player.resetEnergy()
    base.fsm.request('Play', False)
    
