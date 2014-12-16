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

def init(n):
    if n == 1:
        frame = DirectFrame(frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0), image="resources/victory1.png")
    else:
        frame = DirectFrame(frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0), image="resources/victory2.png")
    
    return frame