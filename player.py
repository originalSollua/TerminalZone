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

#Our class imports
from camMov import CameraMovement
from weapons import *

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerGravity, CardMaker
from panda3d.core import NodePath, BitMask32, TransparencyAttrib, Filename, TextNode
from direct.showbase.DirectObject import DirectObject
class Player(DirectObject):
    
    #using this to be our player
    #define tehings like health in here
    #have to tie the camera to this
    #game manager ->player ->camera as far as instantiating goes
    
    def __init__(self):
        
        #Color values
        self.red = 0
        self.green = 1
        self.blue = 1
        self.oRed = 0
        self.oGreen = 1
        self.oBlue = 1
        
        #Limits use of weapons on menus
        self.canUseWeapons = True
        #Current overheat value
        self.overHeat = 0
        #Amount of overheat reduced per cycle
        self.overHeatCount = .1
        #Flag for overheated weapons
        self.isOverHeated = False

        #Flag for ccritical health 
        self.down = True

        #Create player node
        self.playerNode = NodePath('player')
        self.playerNode.reparentTo(render)
        self.playerNode.setPos(0,-30,30)
        self.playerNode.setScale(1.0)
        
        #Create player model and reparent it to playerNode
        self.playerModel = loader.loadModel("./resources/player")
        self.playerModel.reparentTo(self.playerNode)
        self.playerModel.setPos(0,0,2)

        #Create weapons and store them in a map
        self.rRifle = RecursionRifle(base.camera, len(base.projectileList))
        self.mhBlunder = MHB(base.camera, len(base.projectileList))
        self.kvDuals = KeyValue(base.camera, len(base.projectileList))
        self.weaponMap = {1:self.rRifle, 2:self.mhBlunder, 3:self.kvDuals}
        self.curWeapon = 1

        #Names of weapons for switcching images
        self.weaponNameMap = {1:"./resources/rrName.png", 2:"./resources/mhbName.png", 3:"./resources/kvdName.png"}
        
        #Load all weaponName images in so it doesn't stutter on swap
        self.weaponName = OnscreenImage(self.weaponNameMap[3])
        self.weaponName.setTransparency(True)
        self.weaponName.setImage(self.weaponNameMap[2])
        self.weaponName.setTransparency(True)
        self.weaponName.setImage(self.weaponNameMap[1])
        self.weaponName.setTransparency(True)
        self.weaponName.reparentTo(render2d)
       
        #Hide weapons currently not in use
        self.mhBlunder.hide()
        self.kvDuals.hide()

        #Weapon controls
        self.accept("mouse1", self.fireWeapon)
        self.accept("mouse3", self.swapWeapon)
        
        #Display HUD
        self.hud = OnscreenImage("resources/hud.png")
        self.hud.setTransparency(True)
        self.hud.reparentTo(render2d)
        
        # define player health here
        # try not to re-create the player object, will alter reset these values
        # alernatively, dump player stats off in save file before recreating
        print "Mod:",base.damageMod
        self.maxEnergy = 100/base.damageMod
        self.curEnergy = self.maxEnergy
        self.accept("cnode", self.hit)
        self.accept("pickuphealth", self.energyUpgrade)
        
        #Load font for text nodes
        font = loader.loadFont("./resources/ni7seg.ttf")

        #Text node for health bar
        self.healthLable = TextNode('health field name')
        self.healthLable.setFont(font)
        self.healthLable.setText("Abstraction")
        self.textNodePath = aspect2d.attachNewNode(self.healthLable)
        self.textNodePath.setScale(0.05)
        self.healthLable.setAlign(TextNode.ACenter)
        self.textNodePath.setPos(0, 0, .68)
        self.healthLable.setTextColor(self.red, self.green, self.blue, 1)

        #TextNode for enemy counter
        self.enemiesLeft = TextNode('monsters to kill')
        self.enemiesLeft.setFont(font)
        self.enemiesLeft.setText(str(len(base.enemyList)))
        self.texnp = aspect2d.attachNewNode(self.enemiesLeft)
        self.texnp.setScale(.1)
        self.texnp.setPos(-1.68, 0, -.75)
        self.enemiesLeft.setTextColor(1, 1, 0, 1)
        

        #Health bar
        self.bar = DirectWaitBar(text = "", value = self.curEnergy, range = self.maxEnergy, pos = (0,.4,.95), barColor = (self.red, self.green, self.blue, 1))
        self.bar.setScale(0.5)
        #Usage bar       
        self.usageBar = DirectWaitBar(text = "", value = self.overHeat, range = 100,  pos = (1.25, -.4, -.95), barColor =(1, 0, 0,1))
        self.usageBar.setScale(0.5)

        #Initailize player collision
        self.createColision()
        
        #Add player tasks
        base.taskMgr.add(self.updateUsage, "usagePaint", taskChain='Gametasks')
        base.taskMgr.add(self.hFlicker, "hflicker", taskChain='GameTasks')
        base.taskMgr.add(self.updateCount, "Ecount", taskChain='GameTasks')
        base.taskMgr.add(CameraMovement(self.playerModel).cameraControl, "cameraControl", taskChain='GameTasks')
        base.taskMgr.add(self.overHeatTask, "overHeatTask")
        base.taskMgr.add(self.killFloor, "Kill Floor") 

    #Deducts health and updates health bar
    def hit(self, damage):

        self.curEnergy = self.curEnergy-damage
        self.bar['value'] = self.curEnergy
        
        #If the player dies
        if self.curEnergy <= 0:

            #Hide player HUD elements
            self.hide()

            #Player can't use weapons while dead
            self.canUseWeapons = False

            #Request game over menu from fsm
            base.fsm.request('GameOver', 1)
    
    #Hides all visable elements attached to the player
    def hide(self):

        self.weaponMap[self.curWeapon].reticle.setScale(0) 
        self.weaponMap[self.curWeapon].curScale = 0
        self.weaponMap[self.curWeapon].step = False

        self.textNodePath.hide()
        self.texnp.hide()
        self.hud.setScale(0)
        self.weaponName.setScale(0)
        self.usageBar.hide()
        self.bar.hide()

    #Display all visable elements attached to the player
    def show(self):

        self.textNodePath.show()
        self.texnp.show()
        self.hud.setScale(1)
        self.weaponName.setScale(1)
        self.usageBar.show()
        self.bar.show()
        
        #Reset the reticle for the current weapon   
        if self.curWeapon == 1:
            
            self.weaponMap[1].reticle.setScale(.025)
            self.weaponMap[1].curScale = .025

        elif self.curWeapon == 2:
            
            self.weaponMap[2].reticle.setScale(.075)
            self.weaponMap[2].curScale = .075
        else:

            self.weaponMap[3].reticle.setScale(.025)
            self.weaponMap[3].curScale = .025


    # set the player health to a specific value        
    def adjustHealth(self, value):

        self.curEnergy = value
        self.bar['value'] = self.curEnergy
    
    #Update enemy counter
    def updateCount(self, task):
        self.enemiesLeft.setText(str(len(base.enemyList)))
        return task.cont 
    
    #Update usage bar and color
    def updateUsage(self, task):

        if self.curEnergy > 0:
            if self.overHeat < 50:
                self.usageBar['barColor'] = (.2, 1, .5, 1)
            elif self.overHeat >=50 and self.overHeat <70:
                self.usageBar['barColor'] = (1, 1, .2, 1)
            elif self.overHeat >= 70:
                self.usageBar['barColor'] = (1, 0, 0, 1)
            self.usageBar['value'] = self.overHeat
            if self.isOverHeated:
                self.usageBar['barColor'] = (1, 0, 0, 1)
            
        return task.cont

    #Swaps to next weapon in the map
    def swapWeapon(self):

        #If you're not in a menu
        if self.canUseWeapons:
            
            #Reset weapon delay
            self.weaponMap[self.curWeapon].resetWeapon
            
            #Change to next weapon and hide reticles
            if  self.curWeapon == 1:
            
                self.weaponName.setImage(self.weaponNameMap[2])
                self.weaponName.setTransparency(True)
                self.weaponMap[1].reticle.setScale(0)
                self.weaponMap[1].curScale = 0
                self.weaponMap[1].step = False
          
                self.rRifle.hide()
                self.mhBlunder.show()
            
                self.curWeapon = 2
                self.weaponMap[2].reticle.setScale(.075)
                self.weaponMap[2].curScale = .075
            elif self.curWeapon == 2:
            
                self.weaponName.setImage(self.weaponNameMap[3])
                self.weaponName.setTransparency(True)
                self.weaponMap[2].reticle.setScale(0)
                self.weaponMap[2].curScale = 0
                self.weaponMap[2].step = False
            
                self.mhBlunder.hide()
                self.kvDuals.show()
            
                self.curWeapon = 3
                self.weaponMap[3].reticle.setScale(.025)
                self.weaponMap[3].curScale = .025
            elif self.curWeapon == 3:

                self.weaponName.setImage(self.weaponNameMap[1])
                self.weaponName.setTransparency(True)
                self.weaponMap[3].reticle.setScale(0)
                self.weaponMap[3].curScale = 0
                self.weaponMap[3].step = False
            
                self.kvDuals.hide()
                self.rRifle.show()
           
                self.curWeapon = 1
                self.weaponMap[1].reticle.setScale(.025)
                self.weaponMap[1].curScale = .025
         
            base.taskMgr.remove("weaponDelay")
    
    #Fires current weapon
    def fireWeapon(self):

        #If the player is not in a menu
        if self.canUseWeapons:

            #If there isn't a weapon delay task add one
            if base.taskMgr.hasTaskNamed("weaponDelay") == False:
                
                #If your not overheated
                if not self.isOverHeated:

                    base.taskMgr.add(self.weaponMap[self.curWeapon].fire, "fire")

            #If you can shoot as defined by weapon delay
            elif self.weaponMap[self.curWeapon].canShoot() == True:

                #and if your not overheated
                if not self.isOverHeated:
                    
                    base.taskMgr.remove("weaponDelay")
                    base.taskMgr.add(self.weaponMap[self.curWeapon].fire, "fire")

    #Handles weapon overheat
    def overHeatTask(self, task):
        
        #Every cycle decrement your overheat by the specified amount
        self.overHeat -= self.overHeatCount
        
        #If you exceed the limit
        if self.overHeat >= 100:
            
            #Increase cooldown amount and set overheated flag
            self.overHeatCount = .5
            self.isOverHeated = True

        #If your are not overheated anymore reset not default cooldown values
        elif self.overHeat < 0:
            
            self.overHeatCount = .1
            self.overHeat = 0
            self.isOverHeated = False

        return task.cont

    #Initialize player collision
    def createColision(self):
        
        #Set up floor collision handler
        base.floor = CollisionHandlerGravity()
        base.floor.setGravity(9.8)

        #Create player collision node and add to traverser
        self.playerCollNodePath = self.initCollisionSphere(self.playerNode.getChild(0))
        base.cTrav.addCollider(self.playerCollNodePath, base.pusher)
        base.pusher.addCollider(self.playerCollNodePath, self.playerNode)
        
        # Create Floor Ray - for gravity / floor
        floorCollRayPath = self.initCollisionRay(1,-1) 
        base.floor.addCollider(floorCollRayPath, self.playerNode)
        base.cTrav.addCollider(floorCollRayPath, base.floor)
        floorCollRayPath.reparentTo(self.playerModel)

    #Initialize player collision sphere
    def initCollisionSphere(self, obj):
        
        # Create sphere and attach to player
        cNode = CollisionNode('player')

        cs = CollisionSphere(0, 0, 4, 2)
        cNodePath = obj.attachNewNode(CollisionNode('cnode'))
        cNodePath.node().addSolid(cs)
        cNodePath.show()
        
        return cNodePath
    
    #Attach player to a collision ray
    def initCollisionRay(self, originZ, dirZ):
        ray = CollisionRay(0,0,originZ,0,0,dirZ)
        collNode = CollisionNode('playerRay')
        collNode.addSolid(ray)
        collNode.setFromCollideMask(BitMask32.bit(1))
        collNode.setIntoCollideMask(BitMask32.allOff())
        collRayNP = self.playerNode.attachNewNode(collNode)
        collRayNP.show()
        return collRayNP

    #call this method when collide with a health upgrade
    def energyUpgrade(self):

        self.maxEnergy +=(10/base.damageMod)
        self.curEnergy = self.curEnergy+(10/base.damageMod)
        self.bar['range'] = self.maxEnergy
        self.adjustHealth(self.curEnergy)
    
    #Hurts player and resets the to the levels origin upon falliong in a pit.
    def killFloor(self, task):
        
	    z = int(self.playerNode.getPos()[2])

	    if(z < -7):

		    self.playerNode.setPos(0, 0, 6) #resets height
		    self.playerModel.setPos(base.xPos, base.yPos, base.zPos) #resets position
		    self.hit(10)
	    return task.cont

    #Makes the health bar flicker when your health is critical
    def hFlicker(self, task):

        if self.curEnergy <=30:
            if self.down:
                self.red = self.red+0.1
                self.blue = self.blue-.01
                self.green = self.green-.01
            else:
                self.red = self.red-0.1
                self.blue = self.green+0.1
                self.green = self.green+0.1
        else:
            self.red = self.oRed
            self.blue = self.oBlue
            self.green = self.oGreen
        if self.red >=1:
            self.down = False
        if self.red <=0:
            self.down = True
        self.healthLable.setTextColor(self.red, self.green, self.blue, 1)
        self.bar['barColor']=(self.red, self.green, self.blue, 1)
        return task.cont
        
    #Resets players health and signifies they have restarted level after death
    def resetEnergy(self):

        self.canUseWeapons = True
        self.curEnergy = self.maxEnergy
        self.adjustHealth(self.curEnergy)
        

                
