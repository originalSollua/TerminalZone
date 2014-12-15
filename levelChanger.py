#======================================================================#
#
# Team:  
#   Hunter Quant
#   Edward Pryor
#   Nick marasco
#   Shayne Peterson
#   Brandon Williams
#   Jeremy Rose
#
# Last modification: 11/8/14 Jeremy
#
# Description: Changing levels
#                   - Currently when the enemy list is empty
#======================================================================#
import sys

from player import Player
from spawner import Spawner

from panda3d.core import *
from direct.showbase.Transitions import Transitions
from direct.showbase.DirectObject import DirectObject 
from direct.interval.IntervalGlobal import Sequence



class LevelChanger(DirectObject):
    #Use this to handle changing of levels
    #check the emeny list and if it is empty then change the level

    #Flag to tell if the level is complete
    levelComplete = False

    def __init__(self):
        
        self.level01 = "resources/theSouthBridge"
        self.level02 = "resources/theSocket"
        self.level03 = "resources/theDualChannel"
        self.level04 = "resources/theRoot"
        self.levelMap = {1:self.level01, 2:self.level02, 3:self.level03, 4:self.level04}
        self.currentLevel = 1


        #Open file to get player spawns 
        self.pSpawnsFile = open("playerSpawns.txt")
        self.pSpawnsList = self.pSpawnsFile.readlines()
        self.pSpawnsFile.close()
        
        self.spawnIndex = 0
        #Get movement controls
        base.xPos = float(self.pSpawnsList[self.spawnIndex + 1].split("=")[1].translate(None,"\n"))
        base.yPos = float(self.pSpawnsList[self.spawnIndex + 2].split("=")[1].translate(None,"\n"))
        base.zPos = float(self.pSpawnsList[self.spawnIndex + 3].split("=")[1].translate(None,"\n"))
 
        base.player.playerNode.setPos(0, 0, 30) #resets height
        base.player.cameraModel.setPos(base.xPos, base.yPos, base.zPos) #resets position
        print"welcome to levelchanger"

    #checks the enemy list
    #if the list is empty, level is complete
    #set flag to true and change the level.
    def checkLevel (self, task):
        
        enemy = base.spawner.spawnId
        if(len(base.enemyList) == 0):
            if enemy > 0:
                self.levelComplete = True
                if self.currentLevel == len(self.levelMap):
                    base.fsm.request('WinMenu', 1)
                else:
                    self.changeLevel(task)
        
        return task.cont
        

    def changeLevel(self, task):
        if(self.levelComplete == True):
            self.transition = Transitions(loader)
            self.transition.setFadeColor(0, 0, 0)
            self.fadeOut = self.transition.fadeOut(2)

            #unload the current level and models
            self.unload(self.levelMap[self.currentLevel])

            #load the next level and models
            self.load(self.levelMap[self.currentLevel + 1])
            
            #self.fadeIn = self.transition.fadeIn(5)
            base.taskMgr.remove(task)
        return task.cont

    #unloading the stuff not needed
    #like enviroment and stopping sound.
    def unload(self, level):
    
        base.enemyList = []
        print"unloading level.. stop sound, unload level.."
        #stop the music
        base.music.stop()
        
        #detach playerNode
        base.player.playerNode.detachNode()
        
        #Remove enemies
        #base.taskMgr.remove("Spawn Enemies")
        base.taskMgr.remove("enemyCleanup")

        #unload the env and detach remove the node
        base.loader.unloadModel(level)
        base.environ.removeNode()

    def load(self, level):
        
        base.player.adjustHealth(base.player.maxEnergy)

        #load Environment - new level
        base.environ = base.loader.loadModel(level)
        base.environ.reparentTo(base.render)
        base.environ.setScale(7, 7, 3)
        
        #update the currentLevel.
        self.currentLevel += 1

        #reattach player to render
        base.player.playerNode.reparentTo(render)
	    
        self.spawnIndex += 4
        #Get movement controls
        base.xPos = float(self.pSpawnsList[self.spawnIndex + 1].split("=")[1].translate(None,"\n"))
        base.yPos = float(self.pSpawnsList[self.spawnIndex + 2].split("=")[1].translate(None,"\n"))
        base.zPos = float(self.pSpawnsList[self.spawnIndex + 3].split("=")[1].translate(None,"\n"))
        
        base.player.playerNode.setPos(0,0,30) #resets height
        base.player.cameraModel.setPos(base.xPos, base.yPos, base.zPos) #resets position
        
        #create new spawner on the env
        base.spawner = Spawner(base.environ, level.split("/")[1].translate(None,"\n"))
        #Reinit enemies
        base.spawner.spawn()
        base.taskMgr.add(self.checkLevel, "checkLevel")
        base.taskMgr.add(base.enemyCleanUp, "enemyCleanup", taskChain='GameTasks')

        self.fadeIn = self.transition.fadeIn(2)
        base.music.play()
        
    def getCurrentLevel(self):
        return self.currentLevel
        
    def goToBoss(self):
        self.transition = Transitions(loader)
        self.transition.setFadeColor(0, 0, 0)
        self.fadeOut = self.transition.fadeOut(2)
        self.unload(self.levelMap[1])
        self.load(self.levelMap[4])
        self.currentLevel = 4
        
    def resetEnemy(self):
        base.player.cameraModel.setPos(base.xPos, base.yPos, base.zPos)
        base.player.playerNode.setPos(0,0,30) #resets height
        
           
        for i in base.enemyList:
            i.enemyNode.removeNode()
            base.enemyList.remove(i)
          
        base.enemyList = []
        #create new spawner on the env
        base.spawner = Spawner(base.environ, self.levelMap[self.currentLevel].split("/")[1].translate(None,"\n"))
        #Reinit enemies
        base.spawner.spawn()
        
    
                
        
        
                
