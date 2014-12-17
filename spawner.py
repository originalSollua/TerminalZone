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
# Last modification: 12/8/14 By: Brandon
#
# Description: Spawning Enemies
#
#======================================================================#

# Python imports
import sys

# Our class imports
from enemy import Enemy
from boss import Boss

# Panda imports
from direct.showbase.DirectObject import DirectObject

#Handles enemy spawning
class Spawner(DirectObject):
   
    def __init__(self, level, spawnFile):
        
        
        #Reads in enemy spawn locations for current level
        self.eSpawnsFile = open("./enemySpawns/" + spawnFile + "Spawns.txt")
        self.eSpawnsList = self.eSpawnsFile.readlines()
        self.eSpawnsFile.close()
        
        self.enemyX = 0
        self.enemyY = 0
        self.enemyZ = 0
        self.spawnId = 0
        self.offset = 0

    #Gets enemies spawn location
    def spawn(self):
        
        lineIndex = 0
        while lineIndex < len(self.eSpawnsList):
           
            self.enemyX = float(self.eSpawnsList[lineIndex].split("=")[1].translate(None,"\n"))
            self.enemyY = float(self.eSpawnsList[lineIndex + 1].split("=")[1].translate(None,"\n"))
            self.enemyZ = float(self.eSpawnsList[lineIndex + 2].split("=")[1].translate(None,"\n"))
            lineIndex += 3
            self.spawnEnemy(1, self.spawnId)
            
            # Increase enemy count
            self.spawnId += 1

        #If it's the third level add the spawn event trigger
        if base.levelChanger.currentLevel == 3:

           base.taskMgr.add(self.spawnEnemies, "Spawn enemies", taskChain='GameTasks')
	    
        #If it's the fourth level spawn the boss
        if base.levelChanger.currentLevel == 4:

	        self.spawnBoss()      
    
    #Spawns enemy at specified location
    def spawnEnemy(self, modelNum, id):

        if modelNum == 1:
            
            enemyModel = "resources/humanoid"

        else:
            
            print "Invalid Model Number Given"

        enemy = Enemy(enemyModel, id+self.offset)
        enemy.setAI()
        enemy.setPos(self.enemyX, self.enemyY, self.enemyZ)
        base.enemyList.append(enemy)
        self.offset+=1
    
    #On the third level spawns enemies behind the player
    def spawnEnemies(self, task):
        
        if base.player.playerModel.getX() >= 0:

            lineIndex = 0
            while lineIndex < len(self.eSpawnsList):
           
                self.enemyX = -1 * float(self.eSpawnsList[lineIndex].split("=")[1].translate(None,"\n"))
                self.enemyY = -1 * float(self.eSpawnsList[lineIndex + 1].split("=")[1].translate(None,"\n"))
                self.enemyZ = float(self.eSpawnsList[lineIndex + 2].split("=")[1].translate(None,"\n"))
                lineIndex += 3
                self.spawnEnemy(1, self.spawnId*base.levelChanger.currentLevel)
            
                # Increase enemy count
                self.spawnId += 1

            return task.done

        return task.cont
    
    #Spawns the boss on the fourth level
    def spawnBoss(self):

        bossModel = "resources/lordMonkey"
        boss = Boss(bossModel, 9000)

        boss.setPos(-245,245,20)
        boss.setAI()
        base.enemyList.append(boss)
