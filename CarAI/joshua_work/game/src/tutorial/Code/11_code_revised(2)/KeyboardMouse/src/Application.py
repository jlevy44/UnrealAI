from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from FollowCam import FollowCam

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.world = loader.loadModel("environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)

        self.followCam = FollowCam(self.cam, self.panda)

        base.disableMouse()
        props = WindowProperties.getDefault()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)        
        
        self.resetMouse()

        # don't use -repeat because of slight delay after keydown
        self.pandaWalk = False
        self.pandaReverse = False
        self.pandaLeft = False
        self.pandaRight = False

        self.accept("escape", exit)
        self.accept("w", self.beginWalk)
        self.accept("w-up", self.endWalk)
        self.accept("s", self.beginReverse)
        self.accept("s-up", self.endReverse)
        self.accept("a", self.beginTurnLeft)
        self.accept("a-up", self.endTurnLeft)
        self.accept("d", self.beginTurnRight)
        self.accept("d-up", self.endTurnRight)

        taskMgr.add(self.updatePanda, "update panda")

    def resetMouse(self):
        cx = base.win.getProperties().getXSize() / 2
        cy = base.win.getProperties().getYSize() / 2
        base.win.movePointer(0, cx, cy)

    def beginWalk(self):
        self.panda.setPlayRate(1.0, "walk")
        self.panda.loop("walk")
        self.pandaWalk = True

    def endWalk(self):
        self.panda.stop()
        self.pandaWalk = False

    def beginReverse(self):
        self.panda.setPlayRate(-1.0, "walk")
        self.panda.loop("walk")
        self.pandaReverse = True

    def endReverse(self):
        self.panda.stop()
        self.pandaReverse = False

    def beginTurnLeft(self):
        self.pandaLeft = True

    def endTurnLeft(self):
        self.pandaLeft = False

    def beginTurnRight(self):
        self.pandaRight = True

    def endTurnRight(self):
        self.pandaRight = False

    def updatePanda(self, task):
        if base.mouseWatcherNode.hasMouse():
            self.panda.setH(self.panda, -base.mouseWatcherNode.getMouseX() * 10)

        self.resetMouse()

        if self.pandaWalk:
            self.panda.setY(self.panda, -0.2)
        elif self.pandaReverse:
            self.panda.setY(self.panda, 0.2)

        if self.pandaLeft:
            self.panda.setH(self.panda, 0.8)
        elif self.pandaRight:
            self.panda.setH(self.panda, -0.8)

        return task.cont
