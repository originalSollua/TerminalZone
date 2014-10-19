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
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from direct.showbase.DirectObject import DirectObject
class Enemy(DirectObject):
    delFlag = False
    def __init__(self, model, id):
        self.enemyNode = NodePath('enemy'+str(id))
        self.enemyNode.reparentTo(base.render)
        # Load the enemy model, set the scale, and add to render
        self.enemy = Actor(model)
        self.enemy.setScale(0.2,0.2,0.2)
        self.enemy.reparentTo(self.enemyNode)
        
        #configure hit tube
        xTop = self.enemy.getX()
        yTop = self.enemy.getY()
        zTop = self.enemy.getZ()-15
        xBot = xTop
        yBot = yTop
        zBot = zTop-10
        cs = CollisionTube(xTop, yTop, zTop, xBot, yBot, zBot, 20)
        cnodepath = self.enemy.attachNewNode(CollisionNode('cnode'+str(id)))
        cnodepath.node().addSolid(cs)
        cnodepath.show() 
        # so we can walk into the enimies
        self.chand = CollisionHandlerEvent()
        
        # must be same cTrav that was set in player, global collider thing
        base.cTrav.addCollider(cnodepath, self.chand)
        self.accept('cnode'+str(id), self.hite)
    def setPos(self, x, y, z):
		self.enemy.setPos(x, y, z)
        

    def hite(self):
        #access the thing hit like below, the parrent of the collision node
        # damage helth ect below
        self.delFlag = True
