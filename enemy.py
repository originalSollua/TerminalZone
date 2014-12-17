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
# Last modification: 12/8/14 by: Brandon
#
# Description: Represents all the data about an enemy that we could
# ever want.
#
#======================================================================#

#Python imports
import math, random

# Panda imports
from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionSphere, CollisionTube, NodePath
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from direct.showbase.DirectObject import DirectObject
from panda3d.ai import AIWorld, AICharacter

#Our class imports
from player import Player
from pickup import Pickup
from weapons import ScrubCannon

class Enemy(DirectObject):
    
    #Flag for detecting hit enemy
    delFlag = False
    pauseFlag = False

    #Check for peaceful mode
    configFile = open("config.txt")
    configList = configFile.readlines()
    configFile.close()
    peacefulMode = configList[6].split("=")[1].translate(None,"\n")

    def __init__(self, model, id):
        
        self.dontSpawn = False
        self.id = id
        #init and render
        self.enemyNode = NodePath('enemy'+str(id))
        self.AIWorld = AIWorld(base.render)
        self.enemyNode.reparentTo(base.render)

        # Load the enemy model, set the scale, and add to render
        self.enemy =Actor(model,{"walk":"resources/humanoid-walk"})
        self.enemy.reparentTo(self.enemyNode)
        self.enemy.setScale(0.2)

	    #configure hit tube
        self.xTop = self.enemy.getX()
        self.yTop = self.enemy.getY()
        self.zTop = self.enemy.getZ() - 15
        xBot = self.xTop
        yBot = self.yTop
        zBot = self.zTop - 10
        self.cs = CollisionTube(self.xTop, self.yTop, self.zTop, xBot, yBot, zBot, 20)
        
        #init cnode
        self.cnodepath = self.enemy.attachNewNode(CollisionNode('cnode'+str(id)))
        self.cnodepath.setTag('objectTag', str(id))
        self.cnodepath.node().addSolid(self.cs)
        
        #so we can walk into the enemies
        self.chand = CollisionHandlerEvent()
        
        # must be same cTrav that was set in player, global collider thing
        base.cTrav.addCollider(self.cnodepath, self.chand)
        self.accept('cnode'+str(id), self.hit)

        # base settings like damage and health. modify spawner later to change these once we have a more diverse population
        self.health = 20*base.damageMod
        self.damage = 25;
        self.fireDelta = 0
        self.fireOffset = random.randint(0, 200)
        self.deadFlag = False
        self.scrubCannon = ScrubCannon(base.camera, self.enemy)

    #Sets enemy position
    def setPos(self, x, y, z):
		
        #Set enemy position
        self.enemy.setPos(x, y, z)
        
    
    #Checks for being hit by player projectile
    def hit(self, damage):
        
        #access the thing hit like below, the parrent of the collision node
        #damage health etc below
        self.health = self.health-damage
        if self.health <= 0:
            self.delFlag = True
            self.deadFlag = True
            #self.destroy()
        if self.deadFlag and not self.dontSpawn:
            self.spawnPick()
            self.dontSpawn = True

   
    #Fires enemy projecctile
    def fire(self):

        base.taskMgr.add(self.scrubCannon.fire, "fireE")

    #Activate enemy AI
    def setAI(self):
       
    	# Flag this as an AI character
    	#Faster enemy pursue
        self.AIchar = AICharacter("standby", self.enemy, 100,.05,250)
        self.AIWorld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.pursue(base.camera)
        self.AIbehaviors.pauseAi("pursue")

        #Slower enemy pursue
        self.AIchar2 = AICharacter("standby2", self.enemy, 100, .05, 100)
        self.AIWorld.addAiChar(self.AIchar2)
        self.AIbehaviors2 = self.AIchar2.getAiBehaviors()
        self.AIbehaviors2.pursue(base.camera)
        self.AIbehaviors2.pauseAi("pursue")

        base.taskMgr.add(self.AIUpdate, "Update AI")


    #Calculate the distance between the player and the enemy.
    def getDistance(self):

        #get enemy (x,y,z)
        eX = self.enemy.getX()
        eY = self.enemy.getY()
        eZ = self.enemy.getZ()
        
        #get player (x,y,z)
        pX = base.player.playerModel.getX()
        pY = base.player.playerModel.getY()
        pZ = base.player.playerModel.getZ()

        #calculate the distance between the enemy and player (x,y,z)
        #(eX - pX)^2
        x = eX - pX
        x = math.pow(x, 2)

        #(eY - pY)^2
        y = eY - pY
        y = math.pow(y,2)

        #(eZ - pZ)^2
        z = eZ - pZ
        z = math.pow(z, 2)

        self.dist = math.sqrt(x + y + z)
        return self.dist

    #AI behavior
    def AIUpdate(self,task):
        
        #if the enemy is not flaged as dead or paused then we update the AI
        self.max = 200
        self.shoot = 140
        self.min = 50
        if not self.deadFlag:
            if not self.pauseFlag:
                dist = self.getDistance()
                self.pickuppos = self.enemy.getPos()
                #if the distance is less than max, resume the pursue
                if(dist < self.max):
                    self.AIbehaviors.resumeAi("pursue")
                    #also if the distance is less than 'shoot range' then enemies can fire
                    if(dist < self.shoot):
                        self.AIbehaviors.pauseAi("pursue")
                        self.AIbehaviors2.resumeAi("pursue")
                        #if the distance becomes less than the min
                        #pause the chasing and double the firing speed
                        if(dist < self.min):
                            self.fireDelta = self.fireDelta *2
                            self.AIbehaviors.pauseAi("pursue")
                            self.AIbehaviors2.pauseAi("pursue")
                        if(self.peacefulMode != "True"):
                            self.fireDelta+=1
                            if self.fireDelta >= 100+self.fireOffset:
                                self.fireDelta = 0
                                self.fire()
                #else if the distance is more than 200 then don't chase or fire
                elif(dist >200):
                    self.AIbehaviors.pauseAi("pursue")
                    self.AIbehaviors2.pauseAi("pursue")
        else:
            return task.done
        self.AIWorld.update()
        
        return task.cont
    #Pauses enemyies 
    def pause(self):
        
        self.AIbehaviors.pauseAi("pursue")
        self.AIbehaviors2.pauseAi("pursue")
        self.pauseFlag = True

    #Resumes enemies
    def resume(self):

        self.pauseFlag = False
    #Randomly spawns health pickup on enemy death
    def spawnPick(self):

        a = random.randint(0, 100)
        if a > 74:
            base.spawnPickup(self.id, self.pickuppos)            
    
    #Clears enemy from the scene graph upon death
    def destroy(self):

        self.enemyNode.removeNode()
        self.enemy.cleanup()
        self.enemy.removeNode()
        self.cnodepath.node().clearSolids()
        
        base.cTrav.removeCollider(self.cnodepath)
        del self
    
    #Animation currently not functional
    def animate(self):
	
        self.enemy.play("walk")
        self.enemy.loop("walk", fromFrame = 10)
