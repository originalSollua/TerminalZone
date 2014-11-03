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
# Last modification: 10/19/14 By: Nick
#
# Description: Main class to set up environment and run game
#
#======================================================================#

#Python imports
import os, sys

#Our class imports
from player import Player
from enemy import Enemy
from spawner import Spawner

#Panda imports
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import WindowProperties, Filename, Point3
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence


class GameStart(ShowBase):
    
    #Lists for storing entities
    projectileList = []
    enemyList = []

    def __init__(self):
        
        #Start ShowBase
        ShowBase.__init__(self)
       
        #Get window properties, hide the cursor, set properties
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        
        #Disable default mouse controls
        self.disableMouse()

        #Loop music
        self.music = base.loader.loadMusic("./resources/sounds/test.wav")
        self.music.setLoop(True)
        self.music.play()

        #Create new collision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        
        #Load Environment
        self.environ = self.loader.loadModel("resources/chasm")
        self.environ.reparentTo(self.render)
        
        #Debug scalling (0.5, 0.5, 0.5)
        self.environ.setScale(7,7,3)

        #Test load for monkey, will remove later
        self.monkey = self.loader.loadModel("resources/lordMonkey")
        self.monkey.reparentTo(render)
        self.monkey.setScale(3.5,3.5,3.5)

        #Inistialize keys
        self.keyMap = {"w":False, "s":False, "a":False, "d":False, "m":False}

        #Init player here
        self.player = Player()

        #Create spawner open on current level
        self.spawner = Spawner(self.environ)

        #Add tasks
        base.taskMgr.add(self.spawner.checkSpawn, "Spawn Enemies")
        base.taskMgr.add(self.projCleanTask, "Projectile Clean Up")
        base.taskMgr.add(self.enemyCleanUp, "enemyCleanup")

        #Controls
        self.accept("escape", sys.exit, [0])
        
        #WASD controls
        self.accept("w", self.setKey, ["w", True])
        self.accept("s", self.setKey, ["s", True])
        self.accept("a", self.setKey, ["a", True])
        self.accept("d", self.setKey, ["d", True])
        self.accept("m", self.setKey, ["m", True])
        
        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s-up", self.setKey, ["s", False])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("d-up", self.setKey, ["d", False])
        
        #Arrow controls
        self.accept("arrow_up", self.setKey, ["w", True])
        self.accept("arrow_down", self.setKey, ["s", True])
        self.accept("arrow_left", self.setKey, ["a", True])
        self.accept("arrow_right", self.setKey, ["d", True])
        
        self.accept("arrow_up-up", self.setKey, ["w", False])
        self.accept("arrow_down-up", self.setKey, ["s", False])
        self.accept("arrow_left-up", self.setKey, ["a", False])
        self.accept("arrow_right-up", self.setKey, ["d", False])
    
    # Changes the states of the keys pressed
    def setKey(self, key, value):
        
        self.keyMap[key] = value

    def projCleanTask(self, task):
        
        #using this task to find all the projectiles in the projList
        #that have reached the end of their lifespan
        #use the built in destroy to remove them
        for i in self.projectileList:
            
            if i.flag:
               
                i.projectileNode.removeNode()
                self.projectileList.remove(i)
        return task.cont

    def enemyCleanUp(self, task):
        
        #Remove flagged enemies
        for i in self.enemyList:
           
           if i.delFlag:
               
                i.enemyNode.removeNode()
                self.enemyList.remove(i)
                self.spawner.spawnableCount-=1
        return task.cont

TerminalZone = GameStart()
TerminalZone.run()
