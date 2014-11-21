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
from pausemenu import PauseMenu

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
        self.cameraModel = loader.loadModel("models/camera")
        self.cameraModel.reparentTo(self.playerNode)
        #cameraModel.hide()
        self.cameraModel.setPos(0,0,2)
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
        base.taskMgr.add(self.weaponMap[self.curWeapon].over, "overheat")
        
        #HUD
        hud = OnscreenImage("resources/hud.png")
        hud.setTransparency(True)
        hud.reparentTo(render2d)
        
        base.taskMgr.add(CameraMovement(self.cameraModel).cameraControl, "cameraControl")
        self.createColision()
        
        #Calls the pause menu
        self.accept("m", self.startPause)

        # define player health here
        # try not to re-create the player object, will alter reset these values
        # alernatively, dump player stats off in save file before recreating
        self.maxEnergy = 100
        self.curEnergy = self.maxEnergy
		
    
    def hit(self, damage):
        self.curEnergy = self.curEnergy-damage
        print self.curEnergy
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
        elif self.curWeapon == 3:

            self.weaponMap[3].reticle.setScale(0)
            self.weaponMap[3].curScale = 0
            self.weaponMap[3].step = False
            
            self.kvDuals.hide()
            self.rRifle.show()
           
            self.curWeapon = 1
            self.weaponMap[1].reticle.setScale(.025)
            self.weaponMap[1].curScale = .025
         
        base.taskMgr.remove("overheat")
        base.taskMgr.add(self.weaponMap[self.curWeapon].over, "overheat")
    
    def fireWeapon(self):
        print base.taskMgr.hasTaskNamed("fire")
        if base.taskMgr.hasTaskNamed("fire") == False:
            if self.weaponMap[self.curWeapon].getOverHeat() == False:
                base.taskMgr.add(self.weaponMap[self.curWeapon].fire, "fire")
            
        elif self.weaponMap[self.curWeapon].canShoot() == True:
            if self.weaponMap[self.curWeapon].getOverHeat() == False:
                base.taskMgr.remove("fire")
                base.taskMgr.add(self.weaponMap[self.curWeapon].fire, "fire")
            
        else:
            print "Can't Shoot"

    def createColision(self):
        
        # Set up floor collision handler
        base.floor = CollisionHandlerGravity()
        base.floor.setGravity(9.8)

        # Create player collision node and add to traverser
        playerCollNodePath = self.initCollisionSphere(self.playerNode.getChild(0))
        base.cTrav.addCollider(playerCollNodePath, base.pusher)
        base.pusher.addCollider(playerCollNodePath, self.playerNode)
        
        # Create Floor Ray - for gravity / floor
        floorCollRayPath = self.initCollisionRay(1,-1) 
        base.floor.addCollider(floorCollRayPath, self.playerNode)
        base.cTrav.addCollider(floorCollRayPath, base.floor)
	floorCollRayPath.reparentTo(self.cameraModel)

    def initCollisionSphere(self, obj):
        
        # Create sphere and attach to player
        cNode = CollisionNode('player')

        cs = CollisionSphere(0, 0, 4, 2)
        cNodePath = obj.attachNewNode(CollisionNode('cnode'))
        cNodePath.node().addSolid(cs)
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

    def startPause(self):
        
        base.taskMgr.add(PauseMenu(self.playerNode).controlPause, "pauseMenu")

    # call this method when collide with a health upgrade
    def energyUpgrade(self):
        self.maxEnergy +=100
        self.curEnergy = self.maxEnergy
