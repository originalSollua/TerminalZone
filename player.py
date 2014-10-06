#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shane Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/06/14
#
# Description: Player class
# Designed to hold all information about the player.
# Instantiates controls from here by calling to the camMov class.
# Once we have more interesting data about players, it will go here
# note: collisions dont work yet. .egg file needs to flag 
# certain objects as collidable I think
#
#======================================================================#



from camMov import CameraMovement

from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerQueue
from panda3d.core import NodePath, BitMask32

class Player(object):
    #using this to be our player
    #define things like health in here
    #have to tie the camera to this
    #game manager ->player ->camera as far as instantiating goes

    #player variables
    #camera stuck in players head
    global	cam
    global	cm
    
    def __init__(self):
        self.node = NodePath('player')
        self.node.reparentTo(render)
        self.node.setPos(0,15,0)
        self.node.setScale(1.0)
        cameraModel = loader.loadModel("models/camera")
        cameraModel.reparentTo(self.node)
       	cameraModel.hide()
        cameraModel.setPos(0,15,0)
        base.taskMgr.add(CameraMovement(cameraModel).cameraControl, "cameraControl")
        self.createColision()

    def createColision(self):
        colNode = CollisionNode("player")
        colNode.addSolid(CollisionSphere(0, 15, 0, 20))
        solid = self.node.attachNewNode(colNode)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.node, base.drive.node())
        #player vs floor
        ray = CollisionRay()
        #use camera model position
        ray.setOrigin(0, 15, 0)
        ray.setDirection(0, 0, -1)
        colNode = CollisionNode('playerRay')
        colNode.addSolid(ray)
        colNode.setFromCollideMask(BitMask32.bit(0))
        colNode.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(colNode)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
