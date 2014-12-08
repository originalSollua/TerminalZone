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
# Last modification: 12/8/14 by: Brandon
#
# Description: weapon class to have projectiles parented to.
#
#======================================================================#

import os, sys, time
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename
from direct.showbase.ShowBase import ShowBase

from projectile import *

#boss weapon
class ChargeCannon(object):
    #few details needed. just going to spawn a laser at the enemy and move it at us

    def __init__(self, camera, spawnNodePoint):
        self.spawnNode = spawnNodePoint
        self.targetNode = camera

    def fire(self, task):
        
	proj = ChargeProjectile(self.spawnNode, self.targetNode, len(base.projectileList))
	base.taskMgr.add(proj.moveTask, "move projectile")
	base.projectileList.append(proj)
	shotSfx = base.loader.loadSfx("./resources/sounds/charge_cannon.wav")
	shotSfx.setVolume(.5)
	shotSfx.play()

#ScrubCannon - the thing the enemies shoot at us
class ScrubCannon(object):
    #few details needed. just going to spawn a laser at the enemy and move it at us

    def __init__(self, camera, spawnNodePoint):
        self.spawnNode = spawnNodePoint
        self.targetNode = camera

    def fire(self, task):
        
        proj = ScrubProjectile(self.spawnNode, self.targetNode, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = base.loader.loadSfx("./resources/sounds/scrub_cannon.wav")
        shotSfx.setVolume(.4)
        shotSfx.play()


#Recursion Rifle
class RecursionRifle(object):
    
    time = 0
    step = False
    curScale = .025
    delayShot = 0
    overHeat = False
    ohTime = 0
    ttTemp = 1
    ttTempBool = True


    def __init__(self, camera, id):
        #print "guns init"
        #Set model and projectile paths
        self.gunPath = NodePath("gun")
        self.gunPath.reparentTo(base.camera)
        self.gunPath.setPos(1,10,-3.5)
        self.gunModel = loader.loadModel("./resources/rr")
        self.gunModel.reparentTo(self.gunPath)
        self.gunModel.setPos(camera,.7,4,-2)
        self.gunModel.setHpr(90,0,0)
        self.gunModel.setColor(0, 255, 0)
        self.reticle = OnscreenImage("./resources/reticle.png")
        self.reticle.setTransparency(True)
        self.reticle.setScale(self.curScale)
        base.taskMgr.add(self.animate, "rrReticle")

    def fire(self, task):

        #Spawn projectile, add it to taskMgr and play sfx
        proj = RRProjectile(self.gunPath, base.camera, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = base.loader.loadSfx("./resources/sounds/recursion_rifle.wav")
        shotSfx.setVolume(.4)
        shotSfx.play()
        
        self.delayShot = task.time + .8
        base.taskMgr.add(self.contTask, "weaponDelay")
        self.ohTime = self.ohTime + 2
        
        print "Shots fired: ", len(base.projectileList)
        
    def contTask(self, task):
        return task.cont

    def animate(self, task):
    
        if task.time - self.time  > .05:
            
            self.reticle.setScale(self.curScale)
            if self.curScale < .03 and self.step:

                self.curScale += .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale >= .03:

                    self.step = False
            elif self.curScale > .01:

                self.curScale -= .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale <= .01:
                    
                    self.step = True

        return task.cont
    
    def hide(self):
        self.gunModel.hide()

    def show(self):

        self.gunModel.show()
        
    def canShoot(self):
        taskList = base.taskMgr.getTasksNamed("weaponDelay")
        if taskList[0].time >= self.delayShot:
            return True
        else:
            return False
            
    def over(self, task):
        if self.ohTime > 10:
            self.overheat = True
        else:
            self.overheat = False  
             
        if task.time >= self.ttTemp:
            self.ttTemp = self.ttTemp + 1
            self.ttTempBool = True
        if self.ttTemp%1 <= 0:
            if self.ttTempBool == True:
                self.ohTime = self.ohTime - 1
                self.ttTempBool = False
        return task.cont

    def getOverHeat(self):
        return self.overheat
        
    def resetWeapon(self):
        delayShot = 0
        overHeat = False
        ohTime = 0
        ttTemp = 1
        ttTempBool = True

#Max Heao Blunderbuss
class MHB(object):
   
    time = 0
    step = False
    curScale = 0
    hbcount = 0 
    delayShot = 0
    overHeat = False
    ohTime = 0
    ttTemp = 1
    ttTempBool = True
    
    def __init__(self, camera, id):
        
        #Set model and projectile paths
        self.gunPath = NodePath("gun2")
        self.gunPath.reparentTo(base.camera)
        self.gunPath.setPos(1.5,10.5,-3.8)
        self.gunModel = loader.loadModel("./resources/mhb")
        self.gunModel.reparentTo(self.gunPath)
        self.gunModel.setPos(camera, .7,3,-1.4)
        self.gunModel.setHpr(-90,0,0)
        self.reticle = OnscreenImage("./resources/mhbReticle.png")
        self.reticle.setTransparency(True)
        self.reticle.setScale(0)
        base.taskMgr.add(self.animate, "mhbReticle")
        self.gunModel.setColor(0, 0, 0)
    
    def fire(self, task):
        
        #Spawn 20 projectiles, add them to taskMgr and play sfx
        for i in range(1,20):

            proj = MHBProjectile(self.gunPath, base.camera, len(base.projectileList)+self.hbcount, i)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
            self.hbcount+=1
        shotSfx = base.loader.loadSfx("resources/sounds/blunderbuss.wav")
        shotSfx.setVolume(.4)
        shotSfx.play()
        
        self.delayShot = task.time + 1.2
        base.taskMgr.add(self.contTask, "weaponDelay")
        self.ohTime = self.ohTime + 2
        
        print "Shots fired: ", len(base.projectileList)
        
    def contTask(self, task):
        return task.cont

    def animate(self, task):
        
        if task.time - self.time  > .025:
            
            if self.curScale < .08 and self.step:

                self.curScale += .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale == .08:

                    self.step = False
            elif self.curScale > .04:

                self.curScale -= .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale <= .04:
                    
                    self.step = True

        return task.cont
    
    def hide(self):
        
        self.gunModel.hide()

    def show(self):
        
        self.gunModel.show()
        
    def canShoot(self):
        taskList = base.taskMgr.getTasksNamed("weaponDelay")
        print taskList
        if taskList[0].time >= self.delayShot:
            return True
        else:
            return False
            
    def over(self, task):
        if self.ohTime > 10:
            self.overheat = True
        else:
            self.overheat = False  
             
        if task.time >= self.ttTemp:
            self.ttTemp = self.ttTemp + 1
            self.ttTempBool = True
        if self.ttTemp%1 <= 0:
            if self.ttTempBool == True:
                self.ohTime = self.ohTime - 1
                self.ttTempBool = False
        return task.cont

    def getOverHeat(self):
        return self.overheat
    
    def resetWeapon(self):
        delayShot = 0
        overHeat = False
        ohTime = 0
        ttTemp = 1
        ttTempBool = True

class KeyValue(object):
    
    time = 0
    step = False
    curScale = 0
    fireRight = True
    fireLeft = False
    delayShot = 0
    overHeat = False
    ohTime = 0
    ttTemp = 1
    ttTempBool = True

    def __init__(self, camera, id):
       
        #load the other keyValue texture
        keyTexRed = base.loader.loadTexture("resources/tex/keyValueRed.png")
        
        print "guns init"
        #Set model and projectile paths
        self.gunPath1 = NodePath("gun")
        self.gunPath1.reparentTo(base.camera)
        self.gunPath1.setPos(1.2 ,10,-3.5)
        self.gunModel1 = loader.loadModel("./resources/keyValue")
        self.gunModel1.setTexture(keyTexRed,1)
        self.gunModel1.reparentTo(self.gunPath1)
        self.gunModel1.setPos(camera,1.2,4.5,-1.7)
        self.gunModel1.setHpr(-90,0,0)
        #self.gunModel1.setColor(255, 0, 0)

        self.gunPath2 = NodePath("gun")
        self.gunPath2.reparentTo(base.camera)
        self.gunPath2.setPos(-1.2,10,-3.5)
        self.gunModel2 = loader.loadModel("./resources/keyValue")
        self.gunModel2.reparentTo(self.gunPath2)
        self.gunModel2.setPos(camera,-1.2,4.5,-1.7)
        self.gunModel2.setHpr(-90,0,0)
        #self.gunModel2.setColor(0, 0, 255)

        self.reticle = OnscreenImage("./resources/kvReticle.png")
        self.reticle.setTransparency(True)
        self.reticle.setScale(0)
        base.taskMgr.add(self.animate, "kvReticle")

    def fire(self, task):

        if self.fireRight:
            #Spawn projectile, add it to taskMgr and play sfx
            proj = KVProjectile(self.gunPath1, base.camera, len(base.projectileList))
            proj.projectileModel.setColor(0, 0, 255)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
            shotSfx = base.loader.loadSfx("./resources/sounds/recursion_rifle.wav")
            shotSfx.setVolume(.4)
            shotSfx.play()
            self.fireRight = False
            self.fireLeft = True
        else:
            #Spawn projectile, add it to taskMgr and play sfx
            proj = KVProjectile(self.gunPath2, base.camera, len(base.projectileList))
            proj.projectileModel.setColor(255, 0, 0)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
            shotSfx = base.loader.loadSfx("./resources/sounds/recursion_rifle.wav")
            shotSfx.setVolume(.4)
            shotSfx.play()
            self.fireRight = True
            self.fireLeft = False
            
        self.delayShot = task.time + .1
        base.taskMgr.add(self.contTask, "weaponDelay")
        self.ohTime = self.ohTime + 2
        
        print "Shots fired: ", len(base.projectileList)
        
    def contTask(self, task):
        return task.cont

    def animate(self, task):
    
        if task.time - self.time  > .05:
            
            self.reticle.setScale(self.curScale)
            if self.curScale < .03 and self.step:

                self.curScale += .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale >= .03:

                    self.step = False
            elif self.curScale > .01:

                self.curScale -= .001
                self.reticle.setScale(self.curScale)
                self.time = task.time
                if self.curScale <= .01:
                    
                    self.step = True

        return task.cont
   
    def hide(self):

        self.gunModel1.hide()
        self.gunModel2.hide()

    def show(self):

        self.gunModel1.show()
        self.gunModel2.show()
    
    def canShoot(self):
        taskList = base.taskMgr.getTasksNamed("weaponDelay")
        print taskList
        if taskList[0].time >= self.delayShot:
            return True
        else:
            return False
    def over(self, task):
        if self.ohTime > 10:
            self.overheat = True
        else:
            self.overheat = False  
             
        if task.time >= self.ttTemp:
            self.ttTemp = self.ttTemp + 1
            self.ttTempBool = True
        if self.ttTemp%1 <= 0:
            if self.ttTempBool == True:
                self.ohTime = self.ohTime - 1
                self.ttTempBool = False
        return task.cont

    def getOverHeat(self):
        return self.overheat
    
    def resetWeapon(self):
        delayShot = 0
        overHeat = False
        ohTime = 0
        ttTemp = 1
        ttTempBool = True
