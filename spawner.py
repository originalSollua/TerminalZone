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
# Last modification: 10/18/14 By: Nick
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

    def spawn(self, task):
        
        # If there is room, spawn and move an enemy to a random location
        if self.spawnableCount < 20:
            enemy = Enemy()
            enemy.setPos(randint(self.mini[0], self.maxi[0]), randint(self.mini[1], self.maxi[1]), 8)
            self.spawnableCount+= 1

        return task.cont
	

	
