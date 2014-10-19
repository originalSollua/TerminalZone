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
# Last modification: 10/19/14 By: Nick
#
# Description: Spawning Enemies
#
#======================================================================#

# Python imports
from random import randint

# Our class imports
from enemy import Enemy

# Panda imports
from direct.showbase.DirectObject import DirectObject

class Spawner(DirectObject):
   
    def __init__(self, level):
        # Get the maximum and minimum coordinates of the level
        mini, maxi = level.getTightBounds()
        self.mini = [int(mini[0]), int(mini[1])]
        self.maxi = [int(maxi[0]), int(maxi[1])]

        self.spawnableCount = 0

    def checkSpawn(self,task):
        
        # If there is room, spawn and move an enemy to a random location
        if self.spawnableCount < 20:
            # Create new enemy with 'num' model
            self.spawnEnemy(1, self.spawnableCount)

            # Increase enemy count and return task
            self.spawnableCount+= 1
        
        return task.cont
    
    def spawnEnemy(self, modelNum, id):

        if modelNum == 1:
            enemyModel = "resources/humanoid"
        else:
            print "Invalid Model Number Given"

        enemy = Enemy(enemyModel, id)
        enemy.setPos(randint(self.mini[0], self.maxi[0]), randint(self.mini[1], self.maxi[1]), 8)
        base.enemyList.append(enemy)
        del enemy
        print "Enemies: ", len(base.enemyList)
