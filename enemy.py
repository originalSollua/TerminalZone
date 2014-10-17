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
# Last modification: 10/17/14 by: Brandon
#
# Description: Represents all the data about an enemy that we could
# ever want.
#
#======================================================================#

from direct.actor.Actor import Actor


class Enemy(object):

    def __init__(self):
        
        # Load the enemy model, set the scale, and add to render
        self.enemy = Actor("resources/humanoid")
        self.enemy.setScale(0.2,0.2,0.2)
        self.enemy.reparentTo(base.render)
        self.enemy.setPos(0,0,8)

    def setPos(self, x, y, z):
		self.enemy.setPos(x, y, z)
        
