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

def init():
    
    frame = DirectFrame(frameColor=(0,0,0,.5), frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0))
    
    mainMenu = DirectButton(frame,text=("Main Menu","Main Menu","Main Menu","Main Menu"),scale=.1,command=startMain,pressEffect=1,pos=(-.5,0,-.5))
    replay = DirectButton(frame,text=("Restart Level","Restart Level","Restart Level","Restart Level"),scale=.1,command=reLevel,pressEffect=1,pos=(.5,0,-.5))
    
    base.taskMgr.remove("Spawn enemies")
    
    return frame
    
def startMain():
    base.fsm.request('MainMenu')
    
def reLevel():
    base.levelChanger.resetEnemy()
    base.player.resetEnergy()
    base.fsm.request('Play', False)
    
