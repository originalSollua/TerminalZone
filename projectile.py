#======================================================================#
#
# Team:  
#    Hunter Quant
#    Edward Pryor
#	 Nick marasco
#	 Shane Peterson
#    Brandon Williams
#	 Jeremy Rose
#
# Last modification: 10/14/14
#
# Description: Creates a projectile in the world
#
#======================================================================#
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, Vec3, CollisionNode, CollisionSphere, CollisionTraverser, CollisionHandlerEvent
from math import sin, cos
# going to use the system time to calculate when to destroy projectiles
import time
import random
#possible depricated library
from direct.interval.IntervalGlobal import *

class Projectile(DirectObject):
    creaTime = time.clock()
    dur = 2
    vec = 0
    delta = .15
    prevtime = 0
    flag = False
    #defining the thing fired by whatever gun we have

    def __init__(self, camera, look, id):
        #nodepath of the projectile, give it a trajectory
        self.projectileNode = NodePath('projectile'+str(id))
        self.projectileNode.reparentTo(render)
        # by passing the camera node form the camMov object, all projectiles are spawned 5 units in front of the camera
        self.projectileNode.setHpr(look, 0, 0, 0)
        self.projectileNode.setPos(camera,0,3, 3)
        # fix z position to line up with gun
        self.projectileNode.setScale(.1)
        projectileModel = loader.loadModel("./resources/beam.egg")
        projectileModel.reparentTo(self.projectileNode)
    	# must calculate unit vector based on direction
        dir = render.getRelativeVector(look, Vec3(0, 1, 0))
    	#speed up or slow down projectiles here
        dir = dir*10
        self.vec = dir
        
        #base.cTrav = CollisionTraverser()
        cs = CollisionSphere(0, 0, 0, 2.5)
        cnodepath = self.projectileNode.attachNewNode(CollisionNode('projNode'))
        cnodepath.node().addSolid(cs)
        self.collHand = CollisionHandlerEvent()
        self.collHand.addInPattern('into'+str(id))
        self.collHand.addOutPattern('outof')
        #cTrav has the distinction of global colider handler
        base.cTrav.addCollider(cnodepath, self.collHand)
        self.accept('into'+str(id), self.hit)
        
        
        #changing to a move task

      
	#deal with colliding or special effects here.
	#wanted projectiles to be short lived
	# so i will make them delete themselves after impact or time expired
    # writing a task that will rek the projectiles at the end of time
    def moveTask(self, task):
        #curtime = time.clock()
        #self.delta = curtime-self.prevtime
        if self.flag:
            return task.done
        velx = self.vec.x*self.delta
        vely = self.vec.y*self.delta
        velz = self.vec.z*self.delta
        x = self.projectileNode.getX()
        y = self.projectileNode.getY()
        z = self.projectileNode.getZ()
        self.projectileNode.setPos(x+velx, y+vely, z+velz)
        #prevtime = time.clock()
            
        
        if task.time < self.dur:
            return task.cont
        else:
            self.flag = True
            return task.done
        

    def hit(self, collEntry):
        # throw out a custom message for what hit
        if collEntry.getIntoNodePath().getName() != 'projNode':
            temp = collEntry.getIntoNodePath().getName()
            messenger.send(temp) 
            #remove the impacting projectile
            collEntry.getFromNodePath().getParent().getParent().removeNode()
            self.flag =  True

class MHBProjectile(DirectObject):
    creaTime = time.clock()
    dur = .5
    vec = 0
    delta = .15
    prevtime = 0
    flag = False
    #defining the thing fired by whatever gun we have

    def __init__(self, camera, look, id, model):
        #nodepath of the projectile, give it a trajectory
        self.projectileNode = NodePath('projectile'+str(id))
        self.projectileNode.reparentTo(render)
        # by passing the camera node form the camMov object, all projectiles are spawned 5 units in front of the camera
        self.projectileNode.setHpr(look, 0, 0, 0)
        self.projectileNode.setPos(camera,0,3, 3)
        # fix z position to line up with gun
        self.projectileNode.setScale(.1)
        projectileModel = loader.loadModel("./resources/cubeShot.egg")
        projectileModel.reparentTo(self.projectileNode)
    	# must calculate unit vector based on direction
        dir = render.getRelativeVector(look, Vec3(0, 1, 0))
    	#speed up or slow down projectiles here
        dir = dir*10
        self.vec = dir
        if self.vec.x < 2:
            self.vec.x += random.randint(-1,1)
        if self.vec.z < 2:
            self.vec.z += random.randint(-1,1)
        if self.vec.y < 2: 
            self.vec.y += random.randint(-1,1)

        self.vec.x *= random.uniform(.5,1)
        self.vec.y *= random.uniform(.5,1)
        self.vec.z *= random.uniform(.5,1)
        
        
        #base.cTrav = CollisionTraverser()
        cs = CollisionSphere(0, 0, 0, 2.5)
        cnodepath = self.projectileNode.attachNewNode(CollisionNode('projNode'))
        cnodepath.node().addSolid(cs)
        self.collHand = CollisionHandlerEvent()
        self.collHand.addInPattern('into'+str(id))
        self.collHand.addOutPattern('outof')
        #cTrav has the distinction of global colider handler
        base.cTrav.addCollider(cnodepath, self.collHand)
        self.accept('into'+str(id), self.hit)
        
        
        #changing to a move task

      
	#deal with colliding or special effects here.
	#wanted projectiles to be short lived
	# so i will make them delete themselves after impact or time expired
    # writing a task that will rek the projectiles at the end of time
    def moveTask(self, task):
        #curtime = time.clock()
        #self.delta = curtime-self.prevtime
        if self.flag:
            return task.done
        velx = self.vec.x*self.delta
        vely = self.vec.y*self.delta
        velz = self.vec.z*self.delta
        x = self.projectileNode.getX()
        y = self.projectileNode.getY()
        z = self.projectileNode.getZ()
        self.projectileNode.setPos(x+velx, y+vely, z+velz)
        #prevtime = time.clock()
            
        
        if task.time < self.dur:
            return task.cont
        else:
            self.flag = True
            return task.done
        

    def hit(self, collEntry):
        # throw out a custom message for what hit
        if collEntry.getIntoNodePath().getName() != 'projNode':
            temp = collEntry.getIntoNodePath().getName()
            messenger.send(temp) 
            #remove the impacting projectile
            collEntry.getFromNodePath().getParent().getParent().removeNode()
            self.flag =  True
