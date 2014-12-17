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
# Last modification: 11/20/14 By: Shayne
#
# Description: Win Menu that you get when beating the boss
#
#======================================================================#

#Python imports
import sys

#Panda3d imports
from direct.gui.DirectGui import *

#Victory screen menu
def init(n):

    #Switches between 2 victory images
    if n == 1:
        frame = DirectFrame(frameSize=(-1,-1,1,1), pos=(0,0,0))
        base.victoryImage.setImage("./resources/victory1.png")
    else:
        frame = DirectFrame(frameSize=(-1,-1,1,1), pos=(0,0,0))
        base.victoryImage.setImage("./resources/victory2.png")
        
    main = DirectButton(frame,text=("Main Menu","Main Menu","Main Menu","Main Menu"),scale=.1,command=startMain,pressEffect=1,pos=(.05,0,.4))
    
    return frame

#Calls the main menu
def startMain():

    base.victoryImage.hide()
    base.fsm.request('MainMenu', 1)
