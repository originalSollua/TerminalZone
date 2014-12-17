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

    #Spawns boss enemy
    def __init__(self, model, ident):

        Enemy.__init__(self, model, ident)

        self.enemy = Actor(model)
        self.enemy.reparentTo(self.enemyNode)

        self.enemy.setScale(5)
        self.health = 200
        self.damage = 20
        self.weapon = ChargeCannon(base.camera, self.enemy)
        #configure hit tube	
        self.cs = CollisionTube(0, 0, 0, 0, 0, 0, 1.5) 
        #init cnode
        self.cnodepath = self.enemy.attachNewNode(CollisionNode('cnode'+str(id)))
        self.cnodepath.setTag('objectTag', str(id))
        self.cnodepath.node().addSolid(self.cs)
        #so we can walk into the enimies
        self.chand = CollisionHandlerEvent()
        # must be same cTrav that was set in player, global collider thing
        base.cTrav.addCollider(self.cnodepath, self.chand)
        self.accept('cnode'+str(id), self.hit)

    #Fires boss projectile
    def fire(self):
        
        base.taskMgr.add(self.weapon.fire, "boss fire")

    #Adds boss AI
    def setAI(self):

        self.AIChar = AICharacter("boss", self.enemy, 100, .05, 25)
        self.AIWorld.addAiChar(self.AIChar)
        self.AIbehaviors = self.AIChar.getAiBehaviors()

        self.AIbehaviors.pursue(base.camera)

        base.taskMgr.add(self.AIUpdate, "Boss AI Update")
    
    #Updates boss AI
    def AIUpdate(self,task):
        
        if not self.deadFlag:
            if not self.pauseFlag:
                self.AIbehaviors.resumeAi("pursue")
                self.fireDelta+=1
                if self.fireDelta >= 90:
                    self.fireDelta = 0
                    self.fire()
                    self.pickuppos = self.enemy.getPos()
        self.AIWorld.update()
        return Task.cont

    def pause(self):
        self.AIbehaviors.pauseAi("pursue")
        self.pauseFlag = True

    def resume(self):
        #self.AIbehaviors.resumeAi("puruse")
        self.pauseFlag = False
