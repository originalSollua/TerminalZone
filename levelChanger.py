#======================================================================#
#
# Team:  
#   Hunter Quant
#   Edward Pryor
#   Nick marasco
#   Shayne Peterson
#   Brandon Williams
#   Jeremy Rose
#
# Last modification: 11/8/14 Jeremy
#
# Description: Changing levels
#                   - Currently when the enemy list is empty
#======================================================================#
import sys

from player import Player
from spawner import Spawner

from panda3d.core import *
from direct.showbase.Transitions import Transitions
from direct.showbase.DirectObject import DirectObject 
from direct.interval.IntervalGlobal import Sequence



class LevelChanger(DirectObject):
    #Use this to handle changing of levels
    #check the emeny list and if it is empty then change the level

    #Flag to tell if the level is complete
    levelComplete = False 

    def __init__(self):
        self.level01 = "resources/debug"
        self.level02 = "resources/levelWithRoom"
        self.levelMap = {1:self.level01, 2:self.level02}
        print"welcome to levelchanger"

    #checks the enemy list
    #if the list is empty, level is complete
    #set flag to true and change the level.
    def checkLevel (self, task):
        enemy = base.spawner.spawnableCount
        if(len(base.enemyList) == 0):
            if enemy > 0:
                self.levelComplete = True
                self.changeLevel(task)
        

    def changeLevel(self, task):
        if(self.levelComplete == True):
            self.transition = Transitions(loader)
            self.transition.setFadeColor(0, 0, 0)
            self.fadeOut = self.transition.fadeOut(2)

            level = "resources/debug.egg.pz"
            level2 = "resources/chasm"
            
            self.unload(level)
            
            self.load(level2)

            #self.fadeIn = self.transition.fadeIn(5)
            base.taskMgr.remove(task)
        return task.cont

    #unloading the stuff not needed
    #like enviroment and stopping sound.
    def unload(self, level):
        print"unloading level.. stop sound, unload level.."
        #stop the music
        base.music.stop()
        
        #detach playerNode
        base.player.playerNode.detachNode()

        #unload monkey
        base.loader.unloadModel("resources/lordMonkey")

        #detach spawner

        #unload the env and detach remove the node
        base.loader.unloadModel(level)
        base.environ.removeNode()

    def load(self, level):
        #load Environment - new level
        base.environ = base.loader.loadModel(level)
        base.environ.reparentTo(base.render)
        base.environ.setScale(7, 7, 3)

        #load monkey
        base.monkey = base.loader.loadModel("resources/lordMonkey")
        base.monkey.reparentTo(render)
        base.monkey.setScale(3.5, 3.5, 3.5)

        #reattach player to render
        base.player.playerNode.reparentTo(render)
        base.player.playerNode.setPos(0, -30, 30)

        #create new spawner on the env
        base.spawner = Spawner(base.environ)
        self.fadeIn = self.transition.fadeIn(2)
        base.music.play()
                
