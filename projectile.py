from panda3d.core import NodePath
from math import sin, cos


class Projectile(object):
    #defining the thing fired by whatever gun we have

    def __init__(self, x, y, rot):
        self.projectileNode = NodePath('projectile')
        self.projectileNode.reparentTo(render)
	tX = (x*cos(rot %360))-(y*sin(rot %360))
	tY = (x*sin(rot %360))+(y*cos(rot %360))
	print tX
	print tY
        self.projectileNode.setPos(tX,tY, 0)
        self.projectileNode.setScale(.5)
        projectileModel = loader.loadModel("models/panda")
        projectileModel.reparentTo(self.projectileNode)
