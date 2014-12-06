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
# Last modification: 12/5/14 By: Brandon
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

class Spawner(DirectObject):
   
    def __init__(self, level, spawnFile):
        

        self.eSpawnsFile = open("./enemySpawns/" + spawnFile + "Spawns.txt")
        self.eSpawnsList = self.eSpawnsFile.readlines()
        self.eSpawnsFile.close()
        
        self.enemyX = 0
        self.enemyY = 0
        self.enemyZ = 0
        self.spawnId = 0
        self.bossCount = 0
        self.offset = 0

    def spawn(self):
        
        
        lineIndex = 0
        while lineIndex < len(self.eSpawnsList):
           
            self.enemyX = float(self.eSpawnsList[lineIndex].split("=")[1].translate(None,"\n"))
            self.enemyY = float(self.eSpawnsList[lineIndex + 1].split("=")[1].translate(None,"\n"))
            self.enemyZ = float(self.eSpawnsList[lineIndex + 2].split("=")[1].translate(None,"\n"))
            print(self.enemyY)
            lineIndex += 3
            self.spawnEnemy(1, self.spawnId)
            
            # Increase enemy count
            self.spawnId += 1

	    if self.bossCount < 1:

	        #self.spawnBoss()

	        self.bossCount += 1
        
    
    def spawnEnemy(self, modelNum, id):

        if modelNum == 1:
            
            enemyModel = "resources/humanoid"

        else:
            
            print "Invalid Model Number Given"

        enemy = Enemy(enemyModel, id+self.offset)
        enemy.setAI() 
        enemy.setPos(self.enemyX, self.enemyY, self.enemyZ)
        #enemy.animate()
        base.enemyList.append(enemy)
        self.offset+=1
        #print "Enemies: ", len(base.enemyList)

    def spawnBoss(self):

	    bossModel = "resources/lordMonkey"
	    boss = Boss(bossModel, 9000)

	    boss.setPos(-245,245,8)
	    boss.setAI()
	    base.enemyList.append(boss)

