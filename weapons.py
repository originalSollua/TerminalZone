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

#Python imports
import os, sys, time

#Panda3d imports
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename
from direct.showbase.ShowBase import ShowBase
from direct.showbase.Audio3DManager import Audio3DManager

#Our class imports
from projectile import *

#boss weapon
class ChargeCannon(object):
    
    #Gets path for boss projectiles
    def __init__(self, camera, spawnNodePoint):
        
        self.audio3d = Audio3DManager(base.sfxManagerList[0], base.camera)
        self.spawnNode = spawnNodePoint
        self.targetNode = camera

    #Fires boss projectiles
    def fire(self, task):
       
        #Spawn projectile and play sfx
	    proj = ChargeProjectile(self.spawnNode, self.targetNode, len(base.projectileList))
	    base.taskMgr.add(proj.moveTask, "move projectile")
	    base.projectileList.append(proj)
	    shotSfx = self.audio3d.loadSfx("./resources/sounds/charge_cannon.wav")
	    shotSfx.play()

#ScrubCannon - the thing the enemies shoot at us
class ScrubCannon(object):
    
    #Gets path for enemy projectiles
    def __init__(self, camera, spawnNodePoint):

        self.audio3d = Audio3DManager(base.sfxManagerList[0], base.camera)
        self.spawnNode = spawnNodePoint
        self.targetNode = camera

    #Fires enemy projectiles
    def fire(self, task):
        
        #Spawn projectile and play sfx
        proj = ScrubProjectile(self.spawnNode, self.targetNode, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = self.audio3d.loadSfx("./resources/sounds/scrub_cannon.wav")
        shotSfx.play()


#Recursion Rifle
class RecursionRifle(object):
    
    #Amout overheat increases by
    weaponOverHeat = 10

    #For calculating delta time
    time = 0

    #Flag for animation
    step = False

    #Current animation scale
    curScale = .025

    #Delta for shot delay
    delayShot = 0

    def __init__(self, camera, id):
        
        self.audio3d = Audio3DManager(base.sfxManagerList[0], base.camera)
        
        #Get projectile path and gun model
        self.gunPath = NodePath("gun")
        self.gunPath.reparentTo(base.camera)
        self.gunPath.setPos(1,10,-3.5)

        self.gunModel = loader.loadModel("./resources/rr")
        self.gunModel.reparentTo(self.gunPath)
        self.gunModel.setPos(camera,.7,4,-2)
        self.gunModel.setHpr(90,0,0)
        self.gunModel.setColor(0, 255, 0)
        
    #Set gun reticle
        self.reticle = OnscreenImage("./resources/reticle.png")
        self.reticle.setTransparency(True)
        self.reticle.setScale(self.curScale)
        base.taskMgr.add(self.animate, "rrReticle")

    #Hides all visable enlements of the gun
    def hide(self): 
        
        self.reticle.setScale(0)
        self.gunModel.hide()
        self.gunPath.hide()

    #Hides all visable elements of the gun
    def show(self): 
        
        self.gunModel.show()
        self.gunPath.show()

    #Fires recursion rifle
    def fire(self, task):

        #Spawn projectile, add it to taskMgr and play sfx
        proj = RRProjectile(self.gunPath, base.camera, len(base.projectileList))
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        shotSfx = self.audio3d.loadSfx("./resources/sounds/recursion_rifle.wav")
        self.audio3d.attachSoundToObject(shotSfx, base.camera)
        shotSfx.play()
        base.player.overHeat += self.weaponOverHeat
        self.delayShot = task.time + .5
        base.taskMgr.add(self.contTask, "weaponDelay")
    
    #Handles animation of recursion rifle reticle
    def animate(self, task):
    
        #If delta has been long enough
        if task.time - self.time  > .05:
            
            #Update scale
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
    
    #Used to calculate delta for shot delay
    def contTask(self, task):
       
       return task.cont


        
    #You can shoot if the delay has been met
    def canShoot(self):

        taskList = base.taskMgr.getTasksNamed("weaponDelay")
        if taskList[0].time >= self.delayShot:
                   
            return True
        else:
            return False
    
    #Resets delay
    def resetWeapon(self):
        
        delayShot = 0

#Max Heao Blunderbuss
#Comments for this same as recursion rifle for the most part
class MHB(object):

    weaponOverHeat = 33
    time = 0
    step = False
    curScale = 0
    hbcount = 0 
    delayShot = 0
   
    def __init__(self, camera, id):

        self.audio3d = Audio3DManager(base.sfxManagerList[0], base.camera)
        
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
    
    def hide(self): 
        
        self.reticle.setScale(0)
        self.gunModel.hide()
        self.gunPath.hide()

    def show(self): 
        
        self.gunModel.show()
        self.gunPath.show()
    
    def fire(self, task):
        
        #Spawn 20 projectiles, add them to taskMgr and play sfx
        for i in range(1,20):

            proj = MHBProjectile(self.gunPath, base.camera, len(base.projectileList)+self.hbcount, i)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
            self.hbcount+=1
	
        shotSfx = self.audio3d.loadSfx("./resources/sounds/blunderbuss.wav")
        self.audio3d.attachSoundToObject(shotSfx, base.camera)
        shotSfx.play()
        
        base.player.overHeat += self.weaponOverHeat
        self.delayShot = task.time + 1.2
        base.taskMgr.add(self.contTask, "weaponDelay")
        
        
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
    
    def canShoot(self):
        taskList = base.taskMgr.getTasksNamed("weaponDelay")
        
        if taskList[0].time >= self.delayShot:
            return True
        else:
            return False
            

    def getOverHeat(self):
        return self.overheat
    
    def resetWeapon(self):
        
        time = 0
        step = False
        hbcount = 0 
        delayShot = 0
    
#Comments mostly the same as the recursion rifles, but for 2 models.
class KeyValue(object):
    
    weaponOverHeat = 5
    time = 0
    step = False
    curScale = 0
    fireRight = True
    fireLeft = False
    delayShot = 0

    def __init__(self, camera, id):

        self.audio3d = Audio3DManager(base.sfxManagerList[0], base.camera)
       
        #load the other keyValue texture
        keyTexRed = base.loader.loadTexture("resources/tex/keyValueRed.png")
        
        #Set model and projectile paths
        self.gunPath1 = NodePath("gun")
        self.gunPath1.reparentTo(base.camera)
        self.gunPath1.setPos(1.2 ,10,-3.5)
        self.gunModel1 = loader.loadModel("./resources/keyValue")
        self.gunModel1.setTexture(keyTexRed,1)
        self.gunModel1.reparentTo(self.gunPath1)
        self.gunModel1.setPos(camera,1.2,4.5,-1.7)
        self.gunModel1.setHpr(-90,0,0)

        self.gunPath2 = NodePath("gun")
        self.gunPath2.reparentTo(base.camera)
        self.gunPath2.setPos(-1.2,10,-3.5)
        self.gunModel2 = loader.loadModel("./resources/keyValue")
        self.gunModel2.reparentTo(self.gunPath2)
        self.gunModel2.setPos(camera,-1.2,4.5,-1.7)
        self.gunModel2.setHpr(-90,0,0)

        self.reticle = OnscreenImage("./resources/kvReticle.png")
        self.reticle.setTransparency(True)
        self.reticle.setScale(0)
        base.taskMgr.add(self.animate, "kvReticle")

    def hide(self): 
        
        self.reticle.setScale(0)
        self.gunModel1.hide()
        self.gunPath1.hide()
        self.gunModel2.hide()
        self.gunPath2.hide()

    def show(self): 
        
        self.gunModel1.show()
        self.gunPath1.show()
        self.gunModel2.show()
        self.gunPath2.show()
    
    def fire(self, task):

        #Fires left or right
        if self.fireRight:
            
            #Spawn projectile, add it to taskMgr and play sfx
            proj = KVProjectile(self.gunPath1, base.camera, len(base.projectileList))
            proj.projectileModel.setColor(0, 0, 255)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
            shotSfx = self.audio3d.loadSfx("./resources/sounds/key_value.wav")
            self.audio3d.attachSoundToObject(shotSfx, base.camera)
            shotSfx.play()
            self.fireRight = False
            self.fireLeft = True
        else:
            #Spawn projectile, add it to taskMgr and play sfx
            proj = KVProjectile(self.gunPath2, base.camera, len(base.projectileList))
            proj.projectileModel.setColor(255, 0, 0)
            base.taskMgr.add(proj.moveTask, "move projectile")
            base.projectileList.append(proj)
            shotSfx = self.audio3d.loadSfx("./resources/sounds/key_value.wav")
            self.audio3d.attachSoundToObject(shotSfx, base.camera)
            shotSfx.play()
            self.fireRight = True
            self.fireLeft = False
            
        base.player.overHeat += self.weaponOverHeat
        self.delayShot = task.time + .1
        base.taskMgr.add(self.contTask, "weaponDelay")
        
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
   
    def canShoot(self):
        
        taskList = base.taskMgr.getTasksNamed("weaponDelay")
        if taskList[0].time >= self.delayShot:
            return True
        else:
            return False

    def getOverHeat(self):
        
        return self.overheat
    
    def resetWeapon(self):
        
        delayShot = 0
