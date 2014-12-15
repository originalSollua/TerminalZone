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

#from pausemenu import PauseMenu

import sys

from direct.gui.OnscreenImage import OnscreenImage
from math import pi,sin,cos
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

class CameraMovement(DirectObject):
   
    playerNode = 0
    
    # Takes in a cameraModel and sets up key listeners
    def __init__(self, cameraModel):
        
        #Make keyMap globa
        self.keyMap = base.keyMap

        #Reparent camera to cameraModel
        self.cameraModel = cameraModel
        camera.reparentTo(cameraModel)
        camera.setZ(base.camera, 4)

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

        if base.camera.getP() >= 90:

            base.camera.setP(90)
        
        if base.camera.getP() <= -90:

            base.camera.setP(-90)

        # Changes the position of the cameraModel based on which keys are currently pressed
        if(self.keyMap["forward"] == True):
            
            if(self.keyMap["left"] == True):
                
                self.cameraModel.setX(self.cameraModel, -25 * dt)
                self.cameraModel.setY(self.cameraModel, 30 * dt)
                return task.cont
            elif(self.keyMap["right"] == True):
                
                self.cameraModel.setX(self.cameraModel, 25 * dt)
                self.cameraModel.setY(self.cameraModel, 30 * dt)
                return task.cont
            else:
                
                self.cameraModel.setY(self.cameraModel, 30 * dt)
                return task.cont
        elif(self.keyMap["backward"] == True):
            
            if(self.keyMap["left"] == True):
                
                self.cameraModel.setX(self.cameraModel, -25 * dt)
                self.cameraModel.setY(self.cameraModel, -30 * dt)
                return task.cont
            elif(self.keyMap["right"] == True):
                
                self.cameraModel.setX(self.cameraModel, 25 * dt)
                self.cameraModel.setY(self.cameraModel, -30 * dt)
                return task.cont
            else:
                
                self.cameraModel.setY(self.cameraModel, -30 * dt)
                return task.cont
        elif(self.keyMap["left"] == True):
            
            self.cameraModel.setX(self.cameraModel, -25 * dt)
            return task.cont
        elif(self.keyMap["right"] == True):
            
            self.cameraModel.setX(self.cameraModel, 25 * dt)
            return task.cont
        else:
            return task.cont
