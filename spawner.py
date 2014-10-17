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
# Last modification: 10/15/14 By: Brandon Williams
#
# Description: Spawing Enemies
#
#======================================================================#

from random import randint
from direct.showbase.DirectObject import DirectObject

class Spawner(DirectObject):

    def __init__(self, level):
	#get the maximum and minimum coordinates of the level
	mini, maxi = level.getTightBounds()
	self.mini = [int(mini[0]), int(mini[1])]
	self.maxi = [int(maxi[0]), int(maxi[1])]

	self.enemyCount = 0


    def spawnEnemies(self, task):

	if self.enemyCount < 20:
	    enemy = loader.loadModel("resources/humanoid")
	    enemy.setScale(0.2, 0.2, 0.2)
	    enemy.reparentTo(render)
	    enemy.setPos(randint(self.mini[0], self.maxi[0]), randint(self.mini[1], self.maxi[1]), 8)
	    self.enemyCount+= 1

	return task.cont
	

	
