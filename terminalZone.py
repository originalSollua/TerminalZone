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
from direct.gui.OnscreenImage import OnscreenImage


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
        
        #Flag to see if a player has already been spawned
        self.needPlayer = True
        
        #Load in all menu images. If the don't all get set initially, it stutters on switch,
        self.mainMenuImage = OnscreenImage("./resources/mainMenu1.png")
        self.mainMenuImage.setImage("./resources/mainMenu2.png")
        self.mainMenuImage.reparentTo(render2d)
        self.gameOverImage = OnscreenImage("./resources/gameOver1.png")
        self.gameOverImage.setImage("./resources/gameOver2.png")
        self.gameOverImage.reparentTo(render2d)
        self.gameOverImage.hide()
        self.victoryImage = OnscreenImage("./resources/victory1.png")
        self.victoryImage.setImage("./resources/victory2.png")
        self.victoryImage.reparentTo(render2d)
        self.victoryImage.hide()


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

        #Determine prepare to cry mode
        if self.configList[7].split("=")[1].translate(None,"\n") == "True":
            self.damageMod = 2
        else:
            self.damageMod = 1

        #Starts main menu
        self.fsm.request('MainMenu', 1)
        
    def startNewGame(self, load):
        
        #Hide menu background on start of game.
        self.mainMenuImage.hide()
    
        #Get window properties, hide the cursor, set properties
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        
        #Disable default mouse controls
        self.disableMouse()

        #Create new collision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        
        #Init player here
        #If we don't already have a player
        if self.needPlayer:

            self.player = Player()
            self.needPlayer = False

        #Display HUD and set default stats    
        self.player.show()
        self.player.resetEnergy()
        
        #Load first environment
        self.environ = self.loader.loadModel("./resources/theSouthBridge")
        self.environ.reparentTo(self.render)
        self.environ.setScale(7, 7, 3)
        
        #Load skybox
        self.skybox = loader.loadModel("resources/skyBox")
        self.skyboxPath = NodePath(self.skybox)
        self.skyboxPath.setCompass()
        self.skybox.setBin('background',1)
        self.skybox.setDepthWrite(False)
        self.skybox.setLightOff()
        self.skybox.reparentTo(camera)
        
        #Global current player spawn coordinates
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

        #Populate level with enemies
        self.spawner.spawn()
        
        #Add tasks
        #base.taskMgr.add(self.spawner.checkSpawn, "Spawn Enemies", taskChain='GameTasks')
        base.taskMgr.add(self.projCleanTask, "Projectile Clean Up", taskChain='GameTasks')
        base.taskMgr.add(self.enemyCleanUp, "enemyCleanup", taskChain='GameTasks')
        base.taskMgr.add(self.levelChanger.checkLevel, "checkLevel", taskChain='GameTasks')
        base.taskMgr.add(self.pickupClean, "Pickup celeanup", taskChain='GameTasks')
        
        #Get movement controls from config file
        self.forward = self.configList[0].split("=")[1].translate(None,"\n")
        self.backward = self.configList[1].split("=")[1].translate(None,"\n")
        self.left = self.configList[2].split("=")[1].translate(None,"\n")
        self.right = self.configList[3].split("=")[1].translate(None,"\n")

        #Controls
        self.accept("escape", sys.exit, [0])
        self.accept("enter", self.startPause)
        
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

    #Spawn and append pickups to the list
    def spawnPickup(self, id, node):
         
         n = Pickup(id, node)
         self.pickuplist.append(n)

    #Cleans projectiles after impact and specified duration
    def projCleanTask(self, task):
        
        #using this task to find all the projectiles in the projList
        #that have reached the end of their lifespan
        #use the built in destroy to remove them
        for i in self.projectileList:   
            
            if i.flag:
                
                i.projectileNode.removeNode()
                self.projectileList.remove(i)
        return task.cont
    
    #Clears pickups from the environment after collection
    def pickupClean(self, task):

        for i in self.pickuplist:
            
            if i.deletePickup:
                
                i.destroy()
                self.pickuplist.remove(i)
        return task.cont

    #Clears enemies from the environment after being killed or upon player death
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
        
    #Requests pause from the fsm
    def startPause(self):

        self.fsm.request('PauseMenu')
    
    #Handles the delay between menu image swaps
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

#Start game loop
TerminalZone = GameStart()
TerminalZone.run()
