from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bounce import *
import random

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.smiley = loader.loadModel("smiley")
        self.smileyCount = 0
        self.cam.setPos(0, -100, 10)
        taskMgr.doMethodLater(0.1, self.addSmiley, "AddSmiley")
        taskMgr.add(self.updateSmileys, "UpdateSmileys", uponDeath = self.removeSmileys)
        taskMgr.doMethodLater(60, taskMgr.remove, "RemoveUpdate", extraArgs = ["UpdateSmileys"])

    def addSmiley(self, task):
        sm = render.attachNewNode("smiley-instance")
        sm.setPos(random.uniform(-20, 20), random.uniform(-30, 30), random.uniform(0, 30))
        bounce = Bounce()
        bounce.setZ(sm.getZ())
        sm.setPythonTag("bounce", bounce)
        self.smiley.instanceTo(sm)
        self.smileyCount += 1

        if self.smileyCount == 300:
            return task.done

        return task.again

    def updateSmileys(self, task):
        for smiley in render.findAllMatches("smiley-instance"):
            bounce = smiley.getPythonTag("bounce")
            bounce.update()
            smiley.setZ(bounce.getZ())
        return task.cont

    def removeSmileys(self, task):
        for smiley in render.findAllMatches("smiley-instance"):
            smiley.removeNode()
        return task.done