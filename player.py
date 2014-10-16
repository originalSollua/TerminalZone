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

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename
#from pandac.PandaModules import CardMaker, Point2
class Player(object):
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
        cameraModel.hide()
        cameraModel.setPos(0,0,2)

        gunPath = NodePath("gun")
        gunPath.reparentTo(base.camera)
        gunPath.setPos(1,3,-4)
        gunModel = loader.loadModel("resources/gunmodel")
        #gunModel.reparentTo(base.camera)
        gunModel.setPos(-0.4,-1,3.2)
        gunModel.setHpr(0,180,180)
        gunModel.reparentTo(gunPath)
        
        #HUD
        hud = OnscreenImage("./resources/hud.png")
        hud.setTransparency(True)
        hud.reparentTo(render2d)
        
        base.taskMgr.add(CameraMovement(cameraModel, gunPath).cameraControl, "cameraControl")
        self.createColision()


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
