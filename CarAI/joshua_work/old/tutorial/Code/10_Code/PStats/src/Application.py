from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import random

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        PStatClient.connect()
        self.smiley = loader.loadModel("smiley")
        self.smileyCount = 0
        self.cam.setPos(0, -100, 10)
        taskMgr.doMethodLater(0.1, self.addSmiley, "AddSmiley")
        taskMgr.add(self.updateSmileys, "UpdateSmileys", uponDeath = self.removeSmileys)
        taskMgr.doMethodLater(60, taskMgr.remove, "RemoveUpdate", extraArgs = ["UpdateSmileys"])

    def addSmiley(self, task):
        sm = render.attachNewNode("smiley-instance")
        sm.setPos(random.uniform(-20, 20), random.uniform(-30, 30), random.uniform(0, 30))
        sm.setPythonTag("velocity", 0)
        self.smiley.instanceTo(sm)
        self.smileyCount += 1

        if self.smileyCount == 100:
            return task.done

        return task.again

    def updateSmileys(self, task):
        for smiley in render.findAllMatches("smiley-instance"):
            vel = smiley.getPythonTag("velocity")
            z = smiley.getZ()
            if z <= 0:
                vel = random.uniform(0.1, 0.8)
            smiley.setZ(z + vel)
            vel -= 0.01
            smiley.setPythonTag("velocity", vel)
        return task.cont

    def removeSmileys(self, task):
        for smiley in render.findAllMatches("smiley-instance"):
            smiley.removeNode()
        return task.done
