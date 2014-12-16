







from panda3d.core import CollisionSphere, CollisionNode, NodePath, Filename
from direct.showbase.DirectObject import DirectObject
import sys, os
from player import Player

class Pickup(DirectObject):

    def __init__(self, idappend, spawn):
        self.id = "pick"+str(idappend)
        self.deletePickup = False          
        self.projectileNode = NodePath('heal'+str(idappend))

        self.projectileNode.setScale(1)
        self.projectileModel = loader.loadModel("./resources/healthPickup.egg")
        self.projectileModel.setColorScale(200, 0, 0, 100)
        self.projectileModel.reparentTo(self.projectileNode)
        self.projectileNode.reparentTo(render)
        self.projectileNode.setPos(spawn)
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


    def destroy(self):
        self.projectileNode.removeNode()
        self.projectileModel.cleanup()
        self.projectileModel.removeNode()
        #self.cnodepath.node().clearSolids()
        
        #base.cTrav.removeCollider(self.cnodepath)
        del self
