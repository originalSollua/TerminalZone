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
# Last modification: 10/06/14
#
# Description: Main class to set up environment and run game
#
#======================================================================#

import os, sys

from player import Player
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import WindowProperties
from panda3d.core import Point3
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence


class GameStart(ShowBase):
    
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
        # new colision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        # Load Environment
        self.environ = self.loader.loadModel(currentDir + "/resources/test")
        self.environ.reparentTo(self.render)
        self.environ.setScale(0.5,0.5,0.5)
        
        # init player here
        # make camera a part of player
        player = Player()

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
    

TerminalZone = GameStart()
TerminalZone.run()
