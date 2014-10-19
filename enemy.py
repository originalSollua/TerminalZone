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
from panda3d.core import CollisionNode, CollisionSphere, CollisionTube, NodePath

class Enemy(object):

    def __init__(self, model):
        self.enemyNode = NodePath('enemy')
        self.enemyNode.reparentTo(base.render)
        # Load the enemy model, set the scale, and add to render
        self.enemy = Actor(model)
        self.enemy.setScale(0.2,0.2,0.2)
        self.enemy.reparentTo(self.enemyNode)
        
        
        xTop = self.enemy.getX()
        yTop = self.enemy.getY()
        zTop = self.enemy.getZ()-15
        xBot = xTop
        yBot = yTop
        zBot = zTop-10
        cs = CollisionTube(xTop, yTop, zTop, xBot, yBot, zBot, 20)
        cnodepath = self.enemy.attachNewNode(CollisionNode('cnode'))
        cnodepath.node().addSolid(cs)
        cnodepath.show()  

    def setPos(self, x, y, z):
		self.enemy.setPos(x, y, z)
        
