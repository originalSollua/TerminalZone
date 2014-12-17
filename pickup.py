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
# Last modification: 12/16/14
#
# Description: Separate camera controls from the main game
#
#======================================================================#

#Panda3d imports
from panda3d.core import CollisionSphere, CollisionNode, NodePath, Filename, CollisionTraverser, CollisionHandlerEvent
from direct.showbase.DirectObject import DirectObject

#Python imports
import sys, os

#Our class imports
from player import Player

class Pickup(DirectObject):

    #Creates health pickup object
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
        self.accept('pickupin'+str(self.id), self.pickup)
   
    #Detects if the player has picked up the health
    def pickup(self, col):
        
        if col.getIntoNodePath().getName() == "cnode":

            messenger.send("pickuphealth")
            self.deletePickup = True

    #Destroys the health pickups from the scene graph
    def destroy(self):

        self.projectileNode.removeNode()
        self.projectileModel.removeNode()
        self.colNode.node().clearSolids()
        
        del self
