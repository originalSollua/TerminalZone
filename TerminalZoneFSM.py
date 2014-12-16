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
from menus import winmenu

class TerminalZoneFSM(FSM):
    
    tasks = 0
    mm = 0
    pm = 0
    wm = 0

    def __init__(self):
        FSM.__init__(self, "TerminalZoneFSM")
        
    def enterPlay(self, load):
        if (self.tasks != 0):
            for t in self.tasks:
                base.taskMgr.add(t)
            self.tasks = 0
        else:    
            base.startNewGame(load)
    
    def exitPlay(self):
        self.tasks = base.taskMgr.mgr.findTaskChain('GameTasks').getTasks()
        base.taskMgr.mgr.remove(self.tasks)
    
    def enterMainMenu(self, n):
        tasks = 0
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.mm = mainmenu.init(n)
        if n == 1:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["mainmenu1"], appendTask=True)
        else:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["mainmenu2"], appendTask=True)
        
    def exitMainMenu(self):
        base.taskMgr.remove("menu")
        self.mm.destroy()
        
    def enterPauseMenu(self):
        self.pm = pausemenu.init()
    
    def exitPauseMenu(self):
        self.pm.destroy()
        
    def enterGameOver(self, n):
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.gm = gameover.init(n)
        if n == 1:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["gameover1"], appendTask=True)
        else:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["gameover2"], appendTask=True)
        
    def exitGameOver(self):
        base.taskMgr.remove("menu")
        self.gm.destroy()
        
    def enterWinMenu(self, n):
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.wm = winmenu.init(n)
        if n == 1:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["winmenu1"], appendTask=True)
        else:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["winmenu2"], appendTask=True)
            
    def exitWinMenu(self):
        base.taskMgr.remove("menu")
        self.wm.destroy()