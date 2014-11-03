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

from pausemenu import PauseMenu

import sys

from direct.gui.OnscreenImage import OnscreenImage
from math import pi,sin,cos
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from weapons import *
class CameraMovement(DirectObject):
   

    # Takes in a cameraModel and sets up key listeners
    def __init__(self, cameraModel):
        
        self.keyMap = base.keyMap
        self.cameraModel = cameraModel
        camera.reparentTo(cameraModel)
        camera.setZ(base.camera, 4)

    # Determines the movement and pitch of the camera
    def cameraControl(self,task):
        dt = globalClock.getDt()
        if(dt > .20):
            return task.cont
    
        #Calls the pause menu
        if(self.keyMap["m"] == True):
            #self.pm = PauseMenu()
            base.taskMgr.add(PauseMenu().controlPause, "pauseMenu")
            
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
