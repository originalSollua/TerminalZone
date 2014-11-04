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

import os, sys, time
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename
from direct.showbase.ShowBase import ShowBase

from projectile import Projectile, MHBProjectile

#Recursion Rifle
class RecursionRifle(object):
    
    time = 0
    step = False
    curScale = .02


    def __init__(self, camera, id):
                
        #Set model and projectile paths
        self.gunPath = NodePath("gun")
        self.gunPath.reparentTo(base.camera)
        self.gunPath.setPos(1,15,-4)
        self.gunModel = loader.loadModel("resources/gunmodel")
        self.gunModel.reparentTo(self.gunPath)
        self.gunModel.setPos(-.5,-12,3.1)
        self.gunModel.setHpr(0,180,180)
        self.reticle = OnscreenImage("./resources/reticle.png")
        self.reticle.setTransparency(True)
        self.reticle.reparentTo(render2d)
        self.reticle.setScale(self.curScale)
        base.taskMgr.add(self.animate, "reticle")

    def fire(self):

        #Spawn projectile, add it to taskMgr and play sfx
        proj = Projectile(self.gunPath, base.camera, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = base.loader.loadSfx("./resources/sounds/recursion_rifle.wav")
        shotSfx.setVolume(.4)
        shotSfx.play()
        
        print "Shots fired: ", len(base.projectileList)

    def animate(self, task):
    
        if task.time - self.time  > .05:
            if self.curScale < .025 and self.step:

                self.curScale += .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale == .02:

                    self.step = False
            elif self.curScale > .01:

                self.curScale -= .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale <= .01:
                    
                    self.step = True

        return task.cont
        


#Max Heao Blunderbuss
class MHB(object):
   
    def __init__(self, camera, id):
        
        #Set model and projectile paths
        self.gunPath = NodePath("gun")
        self.gunPath.reparentTo(base.camera)
        self.gunPath.setPos(1,8,-4)
        self.gunModel = loader.loadModel("resources/gunmodel")
        self.gunModel.reparentTo(self.gunPath)
        self.gunModel.setPos(-.5,-12,3.1)
        self.gunModel.setHpr(0,180,180)

    def fire(self):
        
        #Spawn 20 projectiles, add them to taskMgr and play sfx
        for i in range(1,20):

            proj = MHBProjectile(self.gunPath, base.camera, len(base.projectileList), i)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
        
        shotSfx = base.loader.loadSfx("resources/sounds/blunderbuss.wav")
        shotSfx.setVolume(.4)
        shotSfx.play()
        
        print "Shots fired: ", len(base.projectileList)
