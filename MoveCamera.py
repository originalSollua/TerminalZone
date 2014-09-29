#======================================================================#
#
# Team:  Hunter Quant
#        Edward Pryor
#        Nick marasco
#        Shane Peterson
#        Brandon Williams
#        Jeremy Rose
#
# Last modification: 09/29/14
#
# Description: Loads camera model with first person perspective. Also,
# gets player input for movement.
#
#======================================================================#



from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3

class MoveCamera(ShowBase):
	
	def setupCamera(self):
		
		#Render the camera model
		self.cameraModel = loader.loadModel("models/camera")
		self.cameraModel.reparentTo(render)
		
		#Attach camera to the parent cameraModel
		self.camera.reparentTo(self.cameraModel)
		
		#Get user input
		self.keyMap =  {"w" : False, "s" : False, "a" : False,  "d" : False}

		self.accept("w-up", self.getKey, ["w", true])
		self.accept("s-up", self.getKey, ["s", true])
		self.accept("a-up", self.getKey, ["a", true])
		self.accept("d-up", self.getKey, ["d", true])
		return self.cameraModel

	def getKey(self, key, value):
		
		self.keyMap[key] = value

	def move(self, task): 
		
		dt = globalClock.getDt
		
		if (dt > .15):
			return task.cont
		
		if (base.mouseWatcherNode.hasMouse == True):
			mousePos = base.mouseWatcherNode.getMouse
			base.camera.setP(mousePos.getY * 25)
			base.camera.setH(mousePOS.getX * -50)

			if (mousePos.getX < .1 and mousePos.getX > -.10):
				self.cameraModel.setH(self.cameraModel.getH)
			else:
				self.cameraModel.setH(self.cameraModel.getH + mousePos.getX * -1)

		if (self.keyMap["w"] == True):
			self.cameraModel.setY(self.cameraModel, 10 * dt)
			return task.cont
		elif (self.keyMap["s"] == True):
			self.cameraModel.setY(self.cameraModel, -10 * dt)
			return task.cont
		elif (self.keyMap["a"] == True):
			self.cameraModel.setX(self.cameraModel, 10 * dt)
			return task.cont
		elif (self.keyMap["d"] == True):
			self.cameraModel.setX(self.cameraModel, -10 * dt)
			return task.cont
		else:
			return task.cont
			
