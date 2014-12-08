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
from panda3d.core import WindowProperties

from menus import mainmenu
from menus import pausemenu
from menus import gameover

class TerminalZoneFSM(FSM):
    
    tasks = 0
    mm = 0
    pm = 0

    def __init__(self):
        FSM.__init__(self, "TerminalZoneFSM")
        
    def enterPlay(self):
        if (self.tasks != 0):
            for t in self.tasks:
                base.taskMgr.add(t)
            self.tasks = 0
        else:    
            base.startNewGame()
    
    def exitPlay(self):
        self.tasks = base.taskMgr.mgr.findTaskChain('GameTasks').getTasks()
        base.taskMgr.mgr.remove(self.tasks)
    
    def enterMainMenu(self):
        self.mm = mainmenu.init()
        
    def exitMainMenu(self):
        self.mm.destroy()
        
    def enterPauseMenu(self):
        self.pm = pausemenu.init()
    
    def exitPauseMenu(self):
        self.pm.destroy()
        
    def enterGameOver(self):
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.gm = gameover.init()
        
    def exitGameOver(self):
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.gm.destroy()