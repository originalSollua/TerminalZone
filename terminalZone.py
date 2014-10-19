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
# Last modification: 10/19/14 By: Nick
#
# Description: Main class to set up environment and run game
#
#======================================================================#

# Python imports
import os, sys

# Our class imports
from player import Player
from enemy import Enemy
from spawner import Spawner

# Panda imports
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import WindowProperties, Filename, Point3
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence


class GameStart(ShowBase):
    
    def __init__(self):
        
        # Start ShowBase
        ShowBase.__init__(self)
        # Get window properties, hide the cursor, set properties
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        # Disable default mouse controls
        self.disableMouse()
        
        # Create new collision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        # Load Environment
        self.environ = self.loader.loadModel("resources/test")
        self.environ.reparentTo(self.render)
        self.environ.setScale(0.5,0.5,0.5)
        
        # Init player here
        # Make camera a part of player
        self.player = Player()

        # Add the random enemy spawning task
        base.taskMgr.add(Spawner(self.environ).spawn, "Spawn Enemies")

TerminalZone = GameStart()
TerminalZone.run()
