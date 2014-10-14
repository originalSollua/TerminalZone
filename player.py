#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shane Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/08/14
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
from panda3d.physics import ActorNode, ForceNode, LinearVectorForce

class Player(object):
    #using this to be our player
    #define things like health in here
    #have to tie the camera to this
    #game manager ->player ->camera as far as instantiating goes

    def __init__(self):
        base.enableParticles()
        self.playerNode = NodePath('player')
        self.playerNode.reparentTo(render)
        self.playerNode.setPos(0,15,0)
        self.playerNode.setScale(1.0)
        cameraModel = loader.loadModel("models/camera")
        cameraModel.reparentTo(self.playerNode)
       	cameraModel.hide()
        cameraModel.setPos(0,0,0)
        base.taskMgr.add(CameraMovement(cameraModel).cameraControl, "cameraControl")
        self.createColision()
#        self.createGravity()

    def createColision(self):
        colNode = CollisionNode("player")
        colNode.addSolid(CollisionSphere(0, 15, 0, 20))
        solid = self.playerNode.attachNewNode(colNode)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.playerNode, base.drive.node())
        #player vs floor
        ray = CollisionRay()
        #use camera model position
        ray.setOrigin(0, 15, 0)
        ray.setDirection(0, 0, -1)
        colNode = CollisionNode('playerRay')
        colNode.addSolid(ray)
        colNode.setFromCollideMask(BitMask32.bit(0))
        colNode.setIntoCollideMask(BitMask32.allOff())
        solid = self.playerNode.attachNewNode(colNode)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)

    def createGravity(self):
        # Create the Nodes to monitor physics
        physicsNode = NodePath("physics")
        physicsNode.reparentTo(render)
        actNode = ActorNode("player-physics")
        actNodeParent = physicsNode.attachNewNode(actNode)
        # Add physics node to the manager
        base.physicsMgr.attachPhysicalNode(actNode)
        self.playerNode.reparentTo(actNodeParent)
        actNode.getPhysicsObject().setMass(90)
        # Create gravity nodes and forces
        gravityFN = ForceNode("dat-grav")
        gravityFNP = render.attachNewNode(gravityFN)
        gravityForce = LinearVectorForce(0,0,-9.81)
        gravityFN.addForce(gravityForce)
        # Add gravity to the manager
        base.physicsMgr.addLinearForce(gravityForce)
