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

from panda3d.core import NodePath
from math import sin, cos


class Projectile(object):
    #defining the thing fired by whatever gun we have

    def __init__(self, camera, look):
        #nodepath of the projectile, give it a trajectory
        self.projectileNode = NodePath('projectile')
        self.projectileNode.reparentTo(render)
        # by passing the camera node form the camMov object, all projectiles are spawned 5 units in front of the camera
        self.projectileNode.setHpr(look, 0, 0, 0)
        self.projectileNode.setPos(camera,0,5, 3)
        # fix z position to line up with gun
        self.projectileNode.setScale(.1)
        projectileModel = loader.loadModel("models/panda")
        projectileModel.reparentTo(self.projectileNode)
