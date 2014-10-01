import os, sys

from camMov import camMov
from panda3d.core import WindowProperties
from panda3d.core import Point3
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence


class MyApp(ShowBase):
    
    def __init__(self):
        
        ShowBase.__init__(self)
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        
        # Get game directory location
        currentDir = os.path.abspath(sys.path[0])
        currentDir = Filename.fromOsSpecific(currentDir).getFullpath()

        # Disable default mouse controls
        self.disableMouse()

        # Load Environment
        self.environ = self.loader.loadModel(currentDir + "/resources/test_level")
        self.environ.reparentTo(self.render)
        self.environ.setScale(0.5,0.5,0.5)
        
        # Add camera task
        cameraModel = loader.loadModel("models/camera")
        cameraModel.reparentTo(render)
        cameraModel.hide()
        cameraModel.setPos(0,15,0)
        cam = camMov(cameraModel)
        self.taskMgr.add(cam.cameraControl, "cameraControl")

        # Load Panda Model
        self.pandaActor = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005,0.005,0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")

        # Create intervals for panda walk
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0,-10,0),
                                                        startPos=Point3(0,10,0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0,10,0),
                                                        startPos=Point3(0,-10,0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180,0,0),
                                                        startHpr=Point3(0,0,0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0,0,0),
                                                        startHpr=Point3(180,0,0))

        # Play animation
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()
    

app = MyApp()
app.run()
