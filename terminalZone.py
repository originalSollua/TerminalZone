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
from pickup import Pickup
from player import Player
from enemy import Enemy
from spawner import Spawner
from levelChanger import LevelChanger
from TerminalZoneFSM import TerminalZoneFSM

#Panda imports
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import WindowProperties, Filename, Point3, NodePath
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence


class GameStart(ShowBase):
   
    #Lists for storing entities
    projectileList = []
    enemyList = []
    pickuplist = []        
    #Initialize keys
    keyMap = {"forward":False, "backward":False, "left":False, "right":False, "m":False}
    fsm = 0
    levelChanger = 0
    player = 0
    
    def __init__(self):
        
        #Start ShowBase
        ShowBase.__init__(self)
        
        #Set up task chain for game play
        base.taskMgr.setupTaskChain('GameTasks')
        
        #start FSM
        self.fsm = TerminalZoneFSM()
        
        #Open file to get configs
        self.configFile = open("config.txt")
        self.configList = self.configFile.readlines()
        self.configFile.close()
        
        #Get and set resolution
        properties = WindowProperties()
        self.xRes = self.configList[4].split("=")[1].translate(None,"\n")
        self.yRes = self.configList[5].split("=")[1].translate(None,"\n")
        properties.setSize(int(self.xRes), int(self.yRes))
        base.win.requestProperties(properties)
        
        #Starts main menu
        self.fsm.request('MainMenu', 1)
        
    def startNewGame(self, load):
    
        #Get window properties, hide the cursor, set properties
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        
        #Disable default mouse controls
        self.disableMouse()

        #Loop music
        self.music = base.loader.loadMusic("./resources/sounds/music.wav")
        self.music.setLoop(True)
        self.music.play()

        #Create new collision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        
        #Init player here
        self.player = Player()
        
        #Load Environment and skybox
        self.environ = self.loader.loadModel("./resources/theSouthBridge")
        self.environ.reparentTo(self.render)
        self.environ.setScale(7, 7, 3)
        
        self.skybox = loader.loadModel("resources/skyBox")
        self.skyboxPath = NodePath(self.skybox)
        self.skyboxPath.setCompass()
        self.skybox.setBin('background',1)
        self.skybox.setDepthWrite(False)
        self.skybox.setLightOff()
        self.skybox.reparentTo(camera)
        
        #Current spawn coordinates
        self.xPos = 0
        self.yPos = 0
        self.zPos = 3
        
        #Create level changer
        self.levelChanger = LevelChanger()
        
        #Check to see if load game was pressed
        if load:
            self.levelChanger.goToBoss()
            #Create spawner open on current level
            self.spawner = Spawner(self.environ, "theRoot")
        else:
            #Create spawner open on current level
            self.spawner = Spawner(self.environ, "theSouthBridge")
        self.spawner.spawn()
        
        #Add tasks
        #base.taskMgr.add(self.spawner.checkSpawn, "Spawn Enemies", taskChain='GameTasks')
        base.taskMgr.add(self.projCleanTask, "Projectile Clean Up", taskChain='GameTasks')
        base.taskMgr.add(self.enemyCleanUp, "enemyCleanup", taskChain='GameTasks')
        base.taskMgr.add(self.levelChanger.checkLevel, "checkLevel", taskChain='GameTasks')
        base.taskMgr.add(self.pickupClean, "Pickup celeanup", taskChain='GameTasks')
        #Get movement controls
        self.forward = self.configList[0].split("=")[1].translate(None,"\n")
        self.backward = self.configList[1].split("=")[1].translate(None,"\n")
        self.left = self.configList[2].split("=")[1].translate(None,"\n")
        self.right = self.configList[3].split("=")[1].translate(None,"\n")

        #Controls
        self.accept("escape", sys.exit, [0])
        self.accept("m", self.startPause)
        
        #Set Controls
        self.accept(self.forward, self.setKey, ["forward", True])
        self.accept(self.backward, self.setKey, ["backward", True])
        self.accept(self.left, self.setKey, ["left", True])
        self.accept(self.right, self.setKey, ["right", True])
        
        self.accept(self.forward+"-up", self.setKey, ["forward", False])
        self.accept(self.backward+"-up", self.setKey, ["backward", False])
        self.accept(self.left+"-up", self.setKey, ["left", False])
        self.accept(self.right+"-up", self.setKey, ["right", False])
    
    # Changes the states of the keys pressed
    def setKey(self, key, value):
        self.keyMap[key] = value

    def spawnPickup(self, id, node):
         n = Pickup(id, node)
         self.pickuplist.append(n)

    def projCleanTask(self, task):
        
        #using this task to find all the projectiles in the projList
        #that have reached the end of their lifespan
        #use the built in destroy to remove them
        for i in self.projectileList:   
            if i.flag:
                i.projectileNode.removeNode()
                self.projectileList.remove(i)
        return task.cont

    def pickupClean(self, task):
        for i in self.pickuplist:
            if i.deletePickup:
                i.destroy()
                self.pickuplist.remove(i)
        return task.cont

    def enemyCleanUp(self, task):

        self.levelChanger.checkLevel(task)
        
        #Remove flagged enemies
        for i in self.enemyList:
           
           if i.delFlag:
               
                #i.enemyNode.removeNode()
                i.destroy()
                self.enemyList.remove(i)
                #self.spawner.spawnableCount-=1
        return task.cont
        
    def startPause(self):
        self.fsm.request('PauseMenu')
        
    def menusTasks(self, s, task):
        if task.time > .75:
            if s == "mainmenu1":
                base.fsm.request('MainMenu', 2)
            elif s == "mainmenu2":
                base.fsm.request('MainMenu', 1)
            elif s == "gameover1":
                base.fsm.request('GameOver', 2)
            elif s == "gameover2":
                base.fsm.request('GameOver', 1)
            elif s == "winmenu1":
                base.fsm.request('WinMenu', 2)
            elif s == "winmenu2":
                base.fsm.request('WinMenu', 1)
        return task.cont

TerminalZone = GameStart()
TerminalZone.run()
