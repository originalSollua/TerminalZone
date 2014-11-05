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
    #define tehings like health in here
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
        self.mhBlunder = MHB(base.camera, len(base.projectileList))
        self.kvDuals = KeyValue(base.camera, len(base.projectileList))
        #Weapons
        self.weaponMap = {1:self.rRifle, 2:self.mhBlunder, 3:self.kvDuals}
        self.curWeapon = 1
        self.mhBlunder.hide()
        self.kvDuals.hide()
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
            
            self.weaponMap[1].reticle.setScale(0)    
            self.weaponMap[1].curScale = 0
            self.weaponMap[1].step = False
           
            self.rRifle.hide()
            self.mhBlunder.show()
            
            self.curWeapon = 2
            self.weaponMap[2].reticle.setScale(.075)
            self.weaponMap[2].curScale = .075
        elif self.curWeapon == 2:
            
            self.weaponMap[2].reticle.setScale(0)
            self.weaponMap[2].curScale = 0
            self.weaponMap[2].step = False
            
            self.mhBlunder.hide()
            self.kvDuals.show()
            
            self.curWeapon = 3
            self.weaponMap[3].reticle.setScale(.025)
            self.weaponMap[3].curScale = .025
        else:
            print "Hello"
            self.weaponMap[3].reticle.setScale(0)
            self.weaponMap[3].curScale = 0
            self.weaponMap[3].step = False
            
            self.kvDuals.hide()
            self.rRifle.show()
            
            self.curWeapon = 1
            self.weaponMap[1].reticle.setScale(.025)
            self.weaponMap[1].curScale = .025


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

