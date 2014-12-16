#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shayne Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/27/14
#
# Description: Pause Menu Class
# This will pause the game and have gui's to select and display a map
# of the level you are on.
#======================================================================#

import sys

from camMov import CameraMovement

from panda3d.core import WindowProperties
from direct.gui.DirectGui import *

def init():

    properties = WindowProperties()
    properties.setCursorHidden(False)
    base.win.requestProperties(properties)
    
    frame = DirectFrame(frameColor=(.2,.2,0,0),frameSize=(base.a2dLeft,base.a2dRight,-1,1),pos=(0,0,0),image="resources/map.png",image_pos=(.65,0,0),image_scale=(.9,0,.9))
    
    resume = DirectButton(frame, text=("Resume Game","Resume Game","Resume Game","Resume Game"), scale=.1, command=resumeGame, pressEffect=1, pos=(-.95,0,.4))
    main = DirectButton(frame, text=("Main Menu","Main Menu","Main Menu","Main Menu"), scale=.1, command=mainMenu, pressEffect=1, pos=(-.95,0,0))
    exit = DirectButton(frame, text=("Exit Game","Exit Game","Exit Game","Exit Game"), scale=.1, command=sys.exit, pressEffect=1, pos=(-.95,0,-.4))
    
    return frame
    
def resumeGame():
    properties = WindowProperties()
    properties.setCursorHidden(True)
    base.win.requestProperties(properties)
    base.fsm.request('Play', False)
    
def mainMenu():
    properties = WindowProperties()
    properties.setCursorHidden(True)
    base.win.requestProperties(properties)
    base.fsm.request('MainMenu', 1)