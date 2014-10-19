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

from panda3d.core import NodePath, Vec3
from math import sin, cos
# going to use the system time to calculate when to destroy projectiles
from datetime import datetime
#possible depricated library
from direct.interval.IntervalGlobal import *

class Projectile(object):
    creaTime = datetime.now().time()
    #defining the thing fired by whatever gun we have

    def __init__(self, camera, look):
        #nodepath of the projectile, give it a trajectory
        self.projectileNode = NodePath('projectile')
        self.projectileNode.reparentTo(render)
        # by passing the camera node form the camMov object, all projectiles are spawned 5 units in front of the camera
        self.projectileNode.setHpr(look, 0, 0, 0)
        self.projectileNode.setPos(camera,0,3, 3)
        # fix z position to line up with gun
        self.projectileNode.setScale(.1)
        projectileModel = loader.loadModel("models/panda")
        projectileModel.reparentTo(self.projectileNode)
	# must calculate unit vector based on direction
	dir = render.getRelativeVector(look, Vec3(0, 1, 0))
	#speed up or slow down projectiles here
	dir = dir*100
    #print dir
	self.trajectory = ProjectileInterval(self.projectileNode,startPos = self.projectileNode.getPos(),startVel = dir, duration = 1, gravityMult = .0001)
	self.trajectory.start()

	#deal with colliding or special effects here.
	#wanted projectiles to be short lived
	# so i will make them delete themselves after impact or time expired
	
    # writing a task that will rek the projectiles at the end of time

	#colide or time up
    def destroy(self):
	self.projectileNode.removeNode()
