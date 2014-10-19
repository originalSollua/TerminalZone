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
# Last modification: 10/19/14 by: Nick
#
# Description: Represents all the data about an enemy that we could
# ever want.
#
#======================================================================#

from direct.actor.Actor import Actor


class Enemy(object):

    def __init__(self, model):
        
        # Load the enemy model, set the scale, and add to render
        self.enemy = Actor(model)
        self.enemy.setScale(0.2,0.2,0.2)
        self.enemy.reparentTo(base.render)

    def setPos(self, x, y, z):
		self.enemy.setPos(x, y, z)
        
