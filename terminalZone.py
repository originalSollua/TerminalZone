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
from levelChanger import LevelChanger

#Panda imports
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import WindowProperties, Filename, Point3, NodePath
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence


class GameStart(ShowBase):
    
    #Lists for storing entities
    projectileList = []
    enemyList = []
        
    #Initialize keys
    keyMap = {"forward":False, "backward":False, "left":False, "right":False, "m":False}
    
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
        self.music = base.loader.loadMusic("./resources/sounds/music.wav")
        self.music.setLoop(True)
        self.music.play()

        #Create new collision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        
        #Load Environment and skybox
        self.environ = self.loader.loadModel("./resources/theRoot")
        self.environ.reparentTo(self.render)
        self.environ.setScale(7, 7, 3)
        
        self.skybox = loader.loadModel("resources/skyBox")
        self.skyTex = loader.loadTexture("resources/tex/skyTex.png")
        self.skyboxPath = NodePath(self.skybox)
        self.skyboxPath.setCompass()
        self.skybox.setBin('background',1)
        self.skybox.setDepthWrite(False)
        self.skybox.setLightOff()
        self.skybox.reparentTo(camera)

        #Debug scalling (0.5, 0.5, 0.5)
        #for chasm, use(7,7,3). will refine scaling standards later.
        #self.environ.setScale(0.5,0.5,0.5)
        #Test load for monkey, will remove later
        self.monkey = self.loader.loadModel("resources/lordMonkey")
        self.monkey.reparentTo(render)
        self.monkey.setScale(3.5,3.5,3.5)
        #Init player here
        self.player = Player()
        
        #Create spawner open on current level
        self.spawner = Spawner(self.environ)

        #Create level changer
        self.levelChanger = LevelChanger()

        #Add tasks
        base.taskMgr.add(self.spawner.checkSpawn, "Spawn Enemies")
        base.taskMgr.add(self.projCleanTask, "Projectile Clean Up")
        base.taskMgr.add(self.enemyCleanUp, "enemyCleanup")
        base.taskMgr.add(self.levelChanger.checkLevel, "checkLevel")

        #Open file to get configs
        self.configFile = open("config.txt")
        self.configList = self.configFile.readlines()

        #Get movement controls
        self.forward = self.configList[0].split("=")[1].translate(None,"\n")
        self.backward = self.configList[1].split("=")[1].translate(None,"\n")
        self.left = self.configList[2].split("=")[1].translate(None,"\n")
        self.right = self.configList[3].split("=")[1].translate(None,"\n")
        
        #Get and set resolution
        self.xRes = self.configList[4].split("=")[1].translate(None,"\n")
        self.yRes = self.configList[5].split("=")[1].translate(None,"\n")
        properties.setSize(int(self.xRes), int(self.yRes))
        base.win.requestProperties(properties) 

        #Controls
        self.accept("escape", sys.exit, [0])
        
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

        self.levelChanger.checkLevel(task)
        
        #Remove flagged enemies
        for i in self.enemyList:
           
           if i.delFlag:
               
                i.enemyNode.removeNode()
                self.enemyList.remove(i)
                #self.spawner.spawnableCount-=1
        return task.cont

TerminalZone = GameStart()
TerminalZone.run()
