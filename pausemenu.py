#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shayne Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/27/14
#
# Description: Pause Menu Class
# This will pause the game and have gui's to select and display a map
# of the level you are on.
#======================================================================#

#Python imports
import sys

#Our class imports
from camMov import CameraMovement

#Panda3d imports
from panda3d.core import *
from panda3d.core import WindowProperties
from panda3d.core import OrthographicLens
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *

class PauseMenu(object):
    
    myAspect = 0
    playerNode = 0
   
    #Creates pause menu
    def __init__(self, playerNode):
    
        self.playerNode = playerNode
        
        pregion = base.win.makeDisplayRegion()
        cam = NodePath(Camera('cam'))
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        cam.node().setLens(lens)
        
        myRender = NodePath('myRender')
        myRender.setDepthTest(False)
        myRender.setDepthWrite(False)
        cam.reparentTo(myRender)
        pregion.setCamera(cam)
        
        aspectRatio = base.getAspectRatio()
        self.myAspect = myRender.attachNewNode(PGTop('myAspect'))
        self.myAspect.setScale(1.0 / aspectRatio, 1.0, 1.0)
        self.myAspect.node().setMouseWatcher(base.mouseWatcherNode)
        
        frame = DirectFrame(frameColor=(0,0,0,.4), frameSize=(base.a2dLeft,base.a2dRight,-1,1), pos=(0,0,0))
        frame.reparentTo(self.myAspect)
        
    
    #control the pause menu   
    def controlPause(self, task):    
        
        exitButton = DirectButton(self.myAspect, text=("Exit","Exit","Exit","Exit"), scale = .1, command = sys.exit, pressEffect=1)
        resumeButton = DirectButton(self.myAspect,text=("Resume Game","Resume Game","Resume Game","Resume Game"),
                                    scale = .1,pressEffect=1,pos=(0,0,.4),command = self.resumeGame)
        
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        
        base.taskMgr.remove("cameraControl")
        base.taskMgr.remove("Spawn Enemies")
    
    #Resumes game
    def resumeGame(self):
    
        cameraModel = loader.loadModel("models/camera")
        cameraModel.reparentTo(self.playerNode)
        base.taskMgr.add(CameraMovement(cameraModel).cameraControl, "cameraControl")
        base.taskMgr.remove("pauseMenu")
        
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.myAspect.removeNode()
        
        
        
        
