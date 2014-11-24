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
# Description: Main Menu for when you start up the game
#
#======================================================================#

import sys

from direct.gui.DirectGui import *

def init():
    
    frame = DirectFrame(frameColor=(0,.2,.1,.1), frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0))
    
    start = DirectButton(frame, text=("New Game","New Game","New Game","New Game"), scale=.1, command=startGame, pressEffect=1, pos=(0,0,.5))
    load = DirectButton(frame, text=("Load Game","Load Game","Load Game","Load Game"), scale=.1, pressEffect=1, pos=(0,0,.25))
    settings = DirectButton(frame, text=("Settings","Settings","Settings","Settings"), scale=.1, pressEffect=1, pos=(0,0,-0.25))
    exit = DirectButton(frame, text=("Exit Game","Exit Game","Exit Game","Exit Game"), scale=.1, command=sys.exit, pressEffect=1, pos=(0,0,-0.5))
    
    return frame
    
def startGame():
    base.fsm.request('Play')