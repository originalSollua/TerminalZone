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

from panda3d.core import *
from panda3d.core import OrthographicLens
from direct.filter.CommonFilters import CommonFilters

class PauseMenu(object):

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
        
        filter = CommonFilters(base.win, cam)
        filter.setBlurSharpen()