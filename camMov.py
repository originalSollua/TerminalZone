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
# Last modification: 10/14/14
#
# Description: Separate camera controls from the main game
#
#======================================================================#

import sys

from math import pi,sin,cos
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from projectile import Projectile
class CameraMovement(DirectObject):
    
    # Takes in a cameraModel and sets up key listeners
    def __init__(self, cameraModel, gunPath):
       
        self.gunPath = gunPath
        self.cameraModel = cameraModel
        camera.reparentTo(cameraModel)
        camera.setZ(base.camera, 4)

        self.keyMap = {"w":False, "s":False, "a":False, "d":False,}

        self.accept("escape", sys.exit, [0])

        self.accept("w", self.setKey, ["w", True])
        self.accept("s", self.setKey, ["s", True])
        self.accept("a", self.setKey, ["a", True])
        self.accept("d", self.setKey, ["d", True])

        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s-up", self.setKey, ["s", False])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("d-up", self.setKey, ["d", False])

        self.accept("mouse1", self.fireWeapon)

    # Changes the states of the keys pressed
    def setKey(self, key, value):
        self.keyMap[key] = value

    def fireWeapon(self):
        proj = Projectile(self.gunPath, base.camera)
        base.taskMgr.add(proj.moveTask, "move projectile")
        base.projectileList.append(proj)
        print "Shots fired: ", len(base.projectileList)
    # Determines the movement and pitch of the camera
    def cameraControl(self,task):
        dt = globalClock.getDt()
        if(dt > .20):
            return task.cont
    
        # Calculate pitch of camera based on mouse position
        mouse = base.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
            self.cameraModel.setH(self.cameraModel.getH() - (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)

        # Changes the position of the cameraModel based on which keys are currently pressed
        if(self.keyMap["w"] == True):
            if(self.keyMap["a"] == True):
                self.cameraModel.setX(self.cameraModel, -10 * dt)
                self.cameraModel.setY(self.cameraModel, 15 * dt)
                return task.cont
            elif(self.keyMap["d"] == True):
                self.cameraModel.setX(self.cameraModel, 10 * dt)
                self.cameraModel.setY(self.cameraModel, 15 * dt)
                return task.cont
            else:
                self.cameraModel.setY(self.cameraModel, 15 * dt)
                return task.cont
        elif(self.keyMap["s"] == True):
            if(self.keyMap["a"] == True):
                self.cameraModel.setX(self.cameraModel, -10 * dt)
                self.cameraModel.setY(self.cameraModel, -15 * dt)
                return task.cont
            elif(self.keyMap["d"] == True):
                self.cameraModel.setX(self.cameraModel, 10 * dt)
                self.cameraModel.setY(self.cameraModel, -15 * dt)
                return task.cont
            else:
                self.cameraModel.setY(self.cameraModel, -15 * dt)
                return task.cont
        elif(self.keyMap["a"] == True):
            self.cameraModel.setX(self.cameraModel, -10 * dt)
            return task.cont
        elif(self.keyMap["d"] == True):
            self.cameraModel.setX(self.cameraModel, 10 * dt)
            return task.cont
        else:
            return task.cont
