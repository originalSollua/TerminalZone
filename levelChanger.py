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

#Python imports
import sys

#Our class imports
from player import Player
from spawner import Spawner

#Panda3d imports
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
        
        #Level map
        self.level01 = "resources/theSouthBridge"
        self.level02 = "resources/theSocket"
        self.level03 = "resources/theDualChannel"
        self.level04 = "resources/theRoot"
        self.levelMap = {1:self.level01, 2:self.level02, 3:self.level03, 4:self.level04}
        self.currentLevel = 1
        
        #Level music map
        self.level01M = base.loader.loadMusic("resources/sounds/level1.wav")
        self.level02M = base.loader.loadMusic("resources/sounds/level2.wav")
        self.level03M = base.loader.loadMusic("resources/sounds/level3.wav")
        self.level04M = base.loader.loadMusic("resources/sounds/bossMusic.wav")
        self.musicMap = {1:self.level01M, 2:self.level02M, 3:self.level03M, 4:self.level04M}

        self.currentMusic = self.musicMap[self.currentLevel]

        self.currentMusic.setLoop(True)
        self.currentMusic.play()

        #Open file to get player spawns 
        self.pSpawnsFile = open("playerSpawns.txt")
        self.pSpawnsList = self.pSpawnsFile.readlines()
        self.pSpawnsFile.close()
        
        #Set players current spawn
        self.spawnIndex = 0
        base.xPos = float(self.pSpawnsList[self.spawnIndex + 1].split("=")[1].translate(None,"\n"))
        base.yPos = float(self.pSpawnsList[self.spawnIndex + 2].split("=")[1].translate(None,"\n"))
        base.zPos = float(self.pSpawnsList[self.spawnIndex + 3].split("=")[1].translate(None,"\n"))
        base.player.playerNode.setPos(0, 0, 30) #resets height
        base.player.playerModel.setPos(base.xPos, base.yPos, base.zPos) #resets position

    #checks the enemy list
    #if the list is empty, level is complete
    #set flag to true and change the level.
    def checkLevel (self, task):
        
        enemy = base.spawner.spawnId
        
        if(len(base.enemyList) == 0):
            if enemy > 0:
                self.levelComplete = True
                if self.currentLevel == len(self.levelMap):
                    base.player.hide()
                    base.player.canUseWeapons = False
                    base.fsm.request('WinMenu', 1)
                    return task.done
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

    #Unloads current level objects
    def unload(self, level):

        for i in base.pickuplist:
           
            i.deletePickup = True
        
        for i in base.enemyList:
            
            i.delFlag = True
            i.deadFlag = True
        
        #stop the music
        self.currentMusic.stop()
        
        #detach playerNode
        base.player.playerNode.detachNode()
        
        #Remove enemies
        #base.taskMgr.remove("Spawn Enemies")
        base.taskMgr.remove("enemyCleanup")

        #unload the env and detach remove the node
        base.loader.unloadModel(level)
        base.environ.removeNode()
    
    #Load the next level
    def load(self, level):
        
        #Reset player health for the next level
        base.player.adjustHealth(base.player.maxEnergy)

        #load Environment - new level
        base.environ = base.loader.loadModel(level)
        base.environ.reparentTo(base.render)
        base.environ.setScale(7, 7, 3)
        
        #update the currentLevel.
        self.currentLevel += 1

        #reattach player to render
        base.player.playerNode.reparentTo(render)
	    
        #Set the next levels spawn coordinates 
        self.spawnIndex += 4
        base.xPos = float(self.pSpawnsList[self.spawnIndex + 1].split("=")[1].translate(None,"\n"))
        base.yPos = float(self.pSpawnsList[self.spawnIndex + 2].split("=")[1].translate(None,"\n"))
        base.zPos = float(self.pSpawnsList[self.spawnIndex + 3].split("=")[1].translate(None,"\n"))
        
        base.player.playerNode.setPos(0,0,30) #resets height
        base.player.playerModel.setPos(base.xPos, base.yPos, base.zPos) #resets position
        
        #create new spawner on the env
        base.spawner = Spawner(base.environ, level.split("/")[1].translate(None,"\n"))
        #Reinit enemies
        base.spawner.spawn()
        base.taskMgr.add(self.checkLevel, "checkLevel")
        base.taskMgr.add(base.enemyCleanUp, "enemyCleanup", taskChain='GameTasks')

        self.fadeIn = self.transition.fadeIn(2)
        
        self.currentMusic = self.musicMap[self.currentLevel]

        self.currentMusic.setLoop(True)
        self.currentMusic.play()
        
    #Returns the current level
    def getCurrentLevel(self):

        return self.currentLevel
    
    #Goes direcctly to the boss level
    def goToBoss(self):

        self.transition = Transitions(loader)
        self.transition.setFadeColor(0, 0, 0)
        self.fadeOut = self.transition.fadeOut(2)
        self.unload(self.levelMap[1])
        self.load(self.levelMap[4])
        self.currentLevel = 4
    
    #Resets enemies upon death
    def resetEnemy(self):

        base.player.playerModel.setPos(base.xPos, base.yPos, base.zPos)
        base.player.playerNode.setPos(0,0,30) #resets height
        
        for i in base.enemyList:
            i.delFlag = True
            i.deadFlag = True
            
        for i in base.pickuplist:
            i.deletePickup = True
            
        #create new spawner on the current level
        base.spawner = Spawner(base.environ, self.levelMap[self.currentLevel].split("/")[1].translate(None,"\n"))
        #Reinit enemies
        base.spawner.spawn()
        
    
                
        
        
                
