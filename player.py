#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shane Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 10/04/14
#
# Description: Player class
# designed to hold all information about the player
# instanciates controles from here byu calling to the camMov class
# once we have more interesting data about players, it will go here
# note: collisions dont work yet. .egg file needs to flag 
# certain objects as collidable i think
#
#======================================================================#



from camMov import camMov

from pandac.PandaModules import*


class Player(object):
	#using this to be our player
	#define things like health in here
	#have to tie the camera to this
	#game manager ->player ->camera as far as instanciating goes
	
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
		base.taskMgr.add(camMov(cameraModel).cameraControl, "cameraControl")
		self.createColision()
	def createColision(self):
		colNode = CollisionNode("player")
		colNode.addSolid(CollisionSphere(0, 15, 0, 20))
		solid = self.node.attachNewNode(colNode)
		base.cTrav.addCollider(solid, base.pusher)
		base.pusher.addCollider(solid, self.node, base.drive.node())
		#player vs floor
		ray = CollisionRay()
		#use camera modle position
		ray.setOrigin(0, 15, 0)
		ray.setDirection(0, 0, -1)
		colNode = CollisionNode('playerRay')
		colNode.addSolid(ray)
		colNode.setFromCollideMask(BitMask32.bit(0))
		colNode.setIntoCollideMask(BitMask32.allOff())
		solid = self.node.attachNewNode(colNode)
		self.nodeGroundHandler = CollisionHandlerQueue()
		base.cTrav.addCollider(solid, self.nodeGroundHandler)
