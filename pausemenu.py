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

from direct.task import Task
from panda3d.core import NodePath

class PauseMenu(object):
    
    def __init__(self):
        
        dr.win.makeDisplayRegion()
        dr.setSort(20)
        self.camera2d = NodePath(Camera('cam2d'))
        lens = OrthographicLens()
        lens.setSize(2, 2)
        lens.setNearFar(-1000, 1000)
        camera2d.node().setLens(lens)
        
        self.pauseNode = NodePath('pause')
        self.pauseNode.setDepthTest(False)
        self.pauseNode.setDepthWrite(False)
        self.pauseNode.reparentTo(pauseNode)
        dr.setCamera(camera2d)
        
        
    #def controlPause(self):
        