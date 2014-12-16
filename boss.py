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
# Last modification: 12/5/14 by: Brandon
# Description: Stuff needed for the boss
#
#======================================================================#

from enemy import Enemy
from weapons import ChargeCannon

from direct.actor.Actor import Actor
from panda3d.ai import AIWorld, AICharacter
from panda3d.core import CollisionNode, CollisionSphere, CollisionTube, NodePath
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from direct.task import Task

class Boss(Enemy):

    def __init__(self, model, ident):

	Enemy.__init__(self, model, ident)

	self.enemy.setScale(2)
	self.health = 150
	self.damage = 20
	self.weapon = ChargeCannon(base.camera, self.enemy)

    def fire(self):
	print "Boss Fire"
	base.taskMgr.add(self.weapon.fire, "boss fire")

    
    def setAI(self):

	self.AIChar = AICharacter("boss", self.enemy, 100, .05, 25)
	self.AIWorld.addAiChar(self.AIChar)
	self.AIbehaviors = self.AIChar.getAiBehaviors()

	self.AIbehaviors.pursue(base.camera)

	base.taskMgr.add(self.AIUpdate, "Boss AI Update")

    def AIUpdate(self,task):

	self.fireDelta+=1
        if self.fireDelta >= 90 and not self.deadFlag:
            self.fireDelta = 0
            self.fire()
            self.pickuppos = self.enemy.getPos()
	self.AIWorld.update()
	return Task.cont
