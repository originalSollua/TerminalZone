#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shane Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/15/14
#
# Description: Player class
# Designed to hold all information about the player.
# Instantiates controls from here by calling to the camMov class.
# Once we have more interesting data about players, it will go here
#
#======================================================================#

from camMov import CameraMovement
from weapons import *

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename
from direct.showbase.DirectObject import DirectObject
class Player(DirectObject):
    
    #using this to be our player
    #define things like health in here
    #have to tie the camera to this
    #game manager ->player ->camera as far as instantiating goes
    
    def __init__(self):
        
        self.playerNode = NodePath('player')
        self.playerNode.reparentTo(render)
        self.playerNode.setPos(0,-30,30)
        
        self.playerNode.setScale(1.0)
        cameraModel = loader.loadModel("models/camera")
        cameraModel.reparentTo(self.playerNode)
        #cameraModel.hide()
        cameraModel.setPos(0,0,2)
        self.rRifle = RecursionRifle(base.camera, len(base.projectileList))
        self.hBlunder = MHB(base.camera, len(base.projectileList))
        #Weapons
        self.weaponMap = {1:self.rRifle, 2:self.hBlunder}
        self.curWeapon = 1
        self.hBlunder.hide()
        self.accept("mouse1", self.fireWeapon)
        self.accept("mouse3", self.swapWeapon)
        
        
        #HUD
        hud = OnscreenImage("resources/hud.png")
        hud.setTransparency(True)
        hud.reparentTo(render2d)
        
        base.taskMgr.add(CameraMovement(cameraModel).cameraControl, "cameraControl")
        self.createColision()

		
    

    def swapWeapon(self): 
        # ignore this print. using it to gather data about the size of the debug room
        print self.playerNode.getPos()
        if  self.curWeapon == 1:
            self.rRifle.hide()
            self.hBlunder.show()
            self.curWeapon = 2
        else:
            self.hBlunder.hide()
            self.rRifle.show()
            self.curWeapon = 1

    def fireWeapon(self):

	    self.weaponMap[self.curWeapon].fire()

    def createColision(self):
        
        # Set up floor collision handler
        base.floor = CollisionHandlerGravity()
        base.floor.setGravity(9.8)

        # Create player collision node and add to traverser
        playerCollNodePath = self.initCollisionSphere(self.playerNode.getChild(0))
        base.cTrav.addCollider(playerCollNodePath, base.pusher)
        base.pusher.addCollider(playerCollNodePath, self.playerNode)
        
        # Create Floor Ray
        floorCollRayPath = self.initCollisionRay(1,-1) 
        base.floor.addCollider(floorCollRayPath, self.playerNode)
        base.cTrav.addCollider(floorCollRayPath, base.floor)

    def initCollisionSphere(self, obj):
        
        # Create sphere and attach to player
        cNode = CollisionNode('player')

        ## Sphere is moved in front of player for testing ##
        cNode.addSolid(CollisionSphere(0,1,4,2))
        cNodePath = obj.attachNewNode(cNode)
        cNodePath.show()
        return cNodePath

    def initCollisionRay(self, originZ, dirZ):
        ray = CollisionRay(0,0,originZ,0,0,dirZ)
        collNode = CollisionNode('playerRay')
        collNode.addSolid(ray)
        collNode.setFromCollideMask(BitMask32.bit(1))
        collNode.setIntoCollideMask(BitMask32.allOff())
        collRayNP = self.playerNode.attachNewNode(collNode)
        collRayNP.show()
        return collRayNP

