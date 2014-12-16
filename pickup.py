







from panda3d.core import CollisionSphere, CollisionNode, NodePath, Filename, CollisionTraverser, CollisionHandlerEvent
from direct.showbase.DirectObject import DirectObject
import sys, os
from player import Player

class Pickup(DirectObject):

    def __init__(self, idappend, spawn):
        self.id = "pick"+str(idappend)
        self.deletePickup = False          
        self.projectileNode = NodePath('heal'+str(self.id))

        self.projectileNode.setScale(1)
        self.projectileModel = loader.loadModel("./resources/healthPickup.egg")
        self.projectileModel.setColorScale(200, 0, 0, 100)
        self.projectileModel.reparentTo(self.projectileNode)
        self.projectileNode.reparentTo(render)
        self.projectileNode.setPos(spawn)
        cs = CollisionSphere(0, 0, 0, .5)
        cnode = CollisionNode('heal')
        self.colNode = self.projectileModel.attachNewNode(cnode)
        self.colNode.node().addSolid(cs)
        self.collHand = CollisionHandlerEvent()
        self.collHand.addInPattern('pickupin'+str(self.id))
        self.collHand.addOutPattern('oot')
        base.cTrav.addCollider(self.colNode, self.collHand)
       # self.model.reparentTo(render)
       # self.model.setPos(x, y-15, z)
        self.accept('pickupin'+str(self.id), self.pickup)
        print "pickup Active"
    def pickup(self, col):
        print col.getIntoNodePath().getName()
        if col.getIntoNodePath().getName() == "cnode":

            print "dolla dolla bills yall"
            messenger.send("pickuphealth")
            self.deletePickup = True

    def destroy(self):
        self.projectileNode.removeNode()
        #self.projectileModel.cleanup()
        self.projectileModel.removeNode()
        self.colNode.node().clearSolids()
        
        #base.cTrav.removeCollider(self.cnodepath)
        del self
