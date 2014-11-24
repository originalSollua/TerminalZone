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
# Description: FSM for Main Menu and Pause Menu
#
#======================================================================#

from direct.fsm.FSM import FSM
from direct.showbase.ShowBase import ShowBase

from menus import mainmenu

class TerminalZoneFSM(FSM):
    
    tasks = 0
    mm = 0

    def __init__(self):
        FSM.__init__(self, "TerminalZoneFSM")
        
    def enterPlay(self):
        base.startNewGame()
    
    def exitPlay(self):
        self.tasks = base.taskMgr.findTaskChain('GameTasks')
        base.taskMgr.remove(self.tasks)
    
    def enterMainMenu(self):
        self.mm = mainmenu.init()
        print "Made it to the Menu"
        
    def exitMainMenu(self):
        #if self.mm != 0:
        self.mm.destroy()