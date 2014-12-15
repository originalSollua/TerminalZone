







from panda3d.core import CollisionSphere, CollisionNode, NodePath
from direct.showbase.DirectObject import DirectObject
from player import Player

class Pickup(DirectObject):

    def __init__(self, idappend, spawn):
        self.id = "pick"+str(idappend)
        self.nnode = NodePath
       
        
        self.projectileNode = NodePath('heal'+str(idappend))
        self.projectileNode.reparentTo(base.render)

        self.projectileNode.setPos(spawn,0,-10, 0)
        self.projectileNode.setScale(.1)
        projectileModel = loader.loadModel("./resources/cubeShot.egg")
        projectileModel.setColorScale(200, 0, 255, 100)
        projectileModel.reparentTo(self.projectileNode)
        self.projectileNode.setHpr(spawn, 0, 0, 0)

       # self.model = loader.loadModel("./resources/sphereShot.egg")
       # self.model.setColorScale(200, 0, 255, 100)
       # cs = CollisionSphere(0, 0, 0, .5)
       # cnode = CollisionNode('heal'+str(self.id))
       # cnode.addSolid(cs)
       # self.colNode = self.model.attachNewNode(cnode)
       # self.model.reparentTo(render)
       # self.model.setPos(x, y-15, z)
       # self.accept("into-"+"heal"+str(self.id), self.pickup)
        print "pickup Active"
    def pickup(self):
        base.messenger.send("pickuphealth", [self.id])

