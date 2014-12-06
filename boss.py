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

from direct.actor.Actor import Actor
from panda3d.ai import AIWorld, AICharacter
from direct.task import Task

class Boss(Enemy):

    def __init__(self, model, ident):

	Enemy.__init__(self, model, ident)
	self.enemy.setScale(5)
	self.health = 150
	self.damage = 35

    def setAI(self):

	self.AIChar = AICharacter("boss", self.enemy, 100, .05, 25)
	self.AIWorld.addAiChar(self.AIChar)
	self.AIbehaviors = self.AIChar.getAiBehaviors()

	self.AIbehaviors.seek(base.camera)

	base.taskMgr.add(self.AIUpdate, "AI Update")

    def AIUpdate(self,task):

	self.AIWorld.update()
	return Task.cont
