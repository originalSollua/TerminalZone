#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shane Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/27/14
#
# Description: Pause Menu Class
# This will pause the game and have gui's to select and display a map
# of the level you are on.
#======================================================================#

import sys

from panda3d.core import *
from panda3d.core import OrthographicLens
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *

class PauseMenu(object):
    
    myAspect = 0
    
    def __init__(self):
        
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
    
    #control the pause menu   
    def controlPause(self, task):    
        exitButton = DirectButton(self.myAspect, text=("Exit","Exit","Exit","Exit"), scale = .1, command = sys.exit)