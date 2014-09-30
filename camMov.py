#======================================================================#
#
# Team:  
#    Hunter Quant
#    Edward Pryor
#    Nick marasco
#    Shane Peterson
#    Brandon Williams
#    Jeremy Rose
#
# Last modification: 09/30/14
#
# Description: External camera controls
#
#======================================================================#

from math import pi,sin,cos
from direct.task import Task

class camMov():
        
    def spinCameraTask(self,task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi/180.0)
        camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians),3)
        camera.setHpr(angleDegrees,0,0)
        return Task.cont

