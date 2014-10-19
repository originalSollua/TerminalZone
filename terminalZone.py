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
# Last modification: 10/16/14
#
# Description: Main class to set up environment and run game
#
#======================================================================#

# System imports
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
    projectileList =[]
    def __init__(self):
        
        # Start ShowBase
        ShowBase.__init__(self)
        # Get window properties, hide the cursor, set properties
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)

        # Disable default mouse controls
        self.disableMouse()
        # new colision system
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        # Load Environment
        self.environ = self.loader.loadModel("resources/test")
        self.environ.reparentTo(self.render)
        self.environ.setScale(0.5,0.5,0.5)
        
        # Init player here
        # Make camera a part of player
        self.player = Player()

        # Init enemy model
        # Class will be setup to take parameters for texture and AIin the future.
        self.enemy = Enemy()
    
	base.taskMgr.add(Spawner(self.environ).spawn, "Spawn Enemies")

TerminalZone = GameStart()
TerminalZone.run()
