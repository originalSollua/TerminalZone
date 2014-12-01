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

from weapons import ScrubCannon
# Panda imports
from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionSphere, CollisionTube, NodePath
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from direct.showbase.DirectObject import DirectObject
from panda3d.ai import AIWorld, AICharacter
from player import Player

class Enemy(DirectObject):
    
    #Flag for detecting hit enemy
    delFlag = False

    #Check for peaceful mode
    configFile = open("config.txt")
    configList = configFile.readlines()
    configFile.close()
    peacefulMode = configList[6].split("=")[1].translate(None,"\n")

    def __init__(self, model, id, ai):
        self.id = id
        #init and render
        self.enemyNode = NodePath('enemy'+str(id))
        self.AIWorld = AIWorld(base.render)
        self.enemyNode.reparentTo(base.render)

        # Load the enemy model, set the scale, and add to render
        self.enemy = Actor(model,{"walk":"resources/humanoid-walk"})
        self.enemy.reparentTo(self.enemyNode)
        #self.enemy.loop("walk")
        self.enemy.setScale(0.2,0.2,0.2)
        #Set behavior
        self.setAI(ai)
        
        #configure hit tube
        xTop = self.enemy.getX()
        yTop = self.enemy.getY()
        zTop = self.enemy.getZ()-15
        xBot = xTop
        yBot = yTop
        zBot = zTop-10
        cs = CollisionTube(xTop, yTop, zTop, xBot, yBot, zBot, 20)
        
        #init cnode
        cnodepath = self.enemy.attachNewNode(CollisionNode('cnode'+str(id)))
        cnodepath.setTag('objectTag', str(id))
        cnodepath.node().addSolid(cs)
        #cnodepath.show()
        
        #so we can walk into the enimies
        self.chand = CollisionHandlerEvent()
        
        # must be same cTrav that was set in player, global collider thing
        base.cTrav.addCollider(cnodepath, self.chand)
        self.accept('cnode'+str(id), self.hit)
        # base settings like damage and health. modify spawner later to change these onec we have a more diverse population
        self.health = 20
        self.damage = 25;
        self.fireDelta = 0
        self.deadFlag = False
        self.scrubCannon = ScrubCannon(base.camera, self.enemy)
    def setPos(self, x, y, z):
		
        #Set enemy position
        self.enemy.setPos(x, y, z)
        

    def hit(self, damage):
        #access the thing hit like below, the parrent of the collision node
        #damage health etc below
        self.health = self.health-damage
        print "Enemy Health:",self.health
        if self.health <= 0:
            self.delFlag = True
            self.enemy.cleanup()
            self.deadFlag = True
            self.destroy()

    def fire(self):
        print "its fire time"
        base.taskMgr.add(self.scrubCannon.fire, "fireE")

    def setAI(self, ai):
       
        if ai == 1:

            # Flag this as an AI character
            self.AIchar = AICharacter("chase", self.enemy, 100,.05,25)
            self.AIWorld.addAiChar(self.AIchar)
            self.AIbehaviors = self.AIchar.getAiBehaviors()

            self.AIbehaviors.pursue(base.camera)
        
        base.taskMgr.add(self.AIUpdate, "Update AI")
    def AIUpdate(self,task):
        if self.peacefulMode == "False":
            self.fireDelta+=1
            if self.fireDelta >= 200 and not self.deadFlag:
                self.fireDelta = 0
                self.fire()
        self.AIWorld.update()
        return task.cont
    def destroy(self):
        del self
