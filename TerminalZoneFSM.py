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

#Panda3d imports
from direct.fsm.FSM import FSM
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

#Our class imports
from menus import mainmenu
from menus import pausemenu
from menus import gameover
from menus import winmenu

#Terminal zone finite state machine
class TerminalZoneFSM(FSM):
    
    tasks = 0
    mm = 0
    pm = 0
    wm = 0

    def __init__(self):
        
        #Set menu music 
        self.menuMusic = base.loader.loadMusic("resources/sounds/menu.wav")
        self.menuMusic.setLoop(True)
        self.menuMusic.play()
        FSM.__init__(self, "TerminalZoneFSM")
    
    #Enters play state
    def enterPlay(self, load):

        self.menuMusic.stop()
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        if (self.tasks != 0):
            for t in self.tasks:
                base.taskMgr.add(t)
            self.tasks = 0
        else:    
            base.startNewGame(load)
    
    #Exits play 
    def exitPlay(self):
        
        self.tasks = base.taskMgr.mgr.findTaskChain('GameTasks').getTasks()
        base.taskMgr.mgr.remove(self.tasks)
    
    #Enter main menu state
    def enterMainMenu(self, n):

        self.tasks = 0
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.mm = mainmenu.init(n)
        if n == 1:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["mainmenu1"], appendTask=True)
        else:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["mainmenu2"], appendTask=True)
    
    #Exit main menu state
    def exitMainMenu(self):

        base.taskMgr.remove("menu")
        self.mm.destroy()
    
    #Enter pause menu state
    def enterPauseMenu(self):

        #Pause the enemies pursue behavior and shooting ability
        for enemy in base.enemyList:
            enemy.pause()
        self.pm = pausemenu.init()
    
    #Exit pause state
    def exitPauseMenu(self):

        #Set the enemy pauseFlag to false allowing enemies to be unpaused
        for enemy in base.enemyList:
            enemy.resume()
        self.pm.destroy()
    
    #Enter game over state   
    def enterGameOver(self, n):

        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.gm = gameover.init(n)
        if n == 1:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["gameover1"], appendTask=True)
        else:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["gameover2"], appendTask=True)
    
    #Exit game over state    
    def exitGameOver(self):

        base.taskMgr.remove("menu")
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.gm.destroy()
    
    #Enter win state
    def enterWinMenu(self, n):

        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.wm = winmenu.init(n)
        if n == 1:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["winmenu1"], appendTask=True)
        else:
            base.taskMgr.add(base.menusTasks, "menu", extraArgs=["winmenu2"], appendTask=True)
    
    #Exit win state
    def exitWinMenu(self):
        
        base.taskMgr.remove("menu")
        self.wm.destroy()
