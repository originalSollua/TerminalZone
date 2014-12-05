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
from random import randint

# Our class imports
from enemy import Enemy
from boss import Boss

# Panda imports
from direct.showbase.DirectObject import DirectObject

class Spawner(DirectObject):
   
    def __init__(self, level):
        
        #Get the maximum and minimum coordinates of the level
        mini, maxi = level.getTightBounds()
        self.mini = [int(mini[0]), int(mini[1])]
        self.maxi = [int(maxi[0]), int(maxi[1])]

        self.spawnableCount = 0
	self.bossCount = 0
        self.offset = 0

    def checkSpawn(self, task):
        
        # If there is room, spawn and move an enemy to a random location
        if self.spawnableCount < 5:
           
            #Create new enemy with 'num' model
            self.spawnEnemy(1, self.spawnableCount)

            # Increase enemy count
            self.spawnableCount+= 1

	if self.bossCount < 1:

	    self.spawnBoss()

	    self.bossCount += 1
        
        return task.cont
    
    def spawnEnemy(self, modelNum, id):

        if modelNum == 1:
            
            enemyModel = "resources/humanoid"

        else:
            
            print "Invalid Model Number Given"

	enemy = Enemy(enemyModel, id+self.offset)
        enemy.setPos(randint(self.mini[0], self.maxi[0]), randint(self.mini[1], self.maxi[1]), 8)
	enemy.setAI()
	enemy.animate()
        base.enemyList.append(enemy)
        self.offset+=1
        #print "Enemies: ", len(base.enemyList)

    def spawnBoss(self):

	bossModel = "resources/lordMonkey"
	boss = Boss(bossModel, 9000)

	boss.setPos(-245,245,8)
	boss.setAI()
	base.enemyList.append(boss)

