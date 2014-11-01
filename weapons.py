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
# Last modification: 10/29/14
#
# Description: weapon class to have projectiles parented to.
#
#======================================================================#

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename

from projectile import Projectile

#Recursion Rifle
class RecursionRifle(object):
   
    def __init__(self, camera, id):
        
        self.gunPath = NodePath("gun")
        self.gunPath.reparentTo(base.camera)
        self.gunModel = loader.loadModel("resources/gunmodel")
        self.gunModel.reparentTo(self.gunPath)
        self.gunPath.setPos(1,15,-4)
        self.gunModel.setPos(-.5,-12,3.1)
        self.gunModel.setHpr(0,180,180)

    def fire(self):

        proj = Projectile(self.gunPath, base.camera, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = base.loader.loadSfx("resources/sounds/recursion_rifle.ogg")
        shotSfx.setVolume(.4)
        shotSfx.play()
        print "Shots fired: ", len(base.projectileList)

#Max Heao Blunderbuss
class MHB(object):
   
    def __init__(self, camera, id):
        
        self.gunPath = NodePath("gun")
        self.gunPath.reparentTo(base.camera)
        self.gunModel = loader.loadModel("resources/gunmodel")
        self.gunModel.reparentTo(self.gunPath)
        self.gunPath.setPos(1,15,-4)
        self.gunModel.setPos(-.5,-12,3.1)
        self.gunModel.setHpr(0,180,180)

    def fire(self):

        proj = Projectile(self.gunPath, base.camera, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = base.loader.loadSfx("resources/sounds/recursion_rifle.ogg")
        shotSfx.setVolume(.4)
        shotSfx.play()
        print "Shots fired: ", len(base.projectileList)
