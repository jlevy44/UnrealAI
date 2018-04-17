from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import random

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(0, -100, 10)
        self.setFrameRateMeter(True)

        envRoot = render.attachNewNode("envRoot")
        for i in range(100):
            self.addEnvironment(envRoot)
        envRoot.flattenStrong()

        combiner = RigidBodyCombiner("cmb")
        self.smRoot = render.attachNewNode(combiner)
        for i in range(200):
            self.addSmiley(self.smRoot)
        combiner.collect()
        taskMgr.add(self.updateSmileys, "UpdateSmileys")

    def addSmiley(self, parent):
        sm = loader.loadModel("smiley")
        sm.reparentTo(parent)
        sm.setPos(random.uniform(-20, 20), random.uniform(-30, 30), random.uniform(0, 30))
        sm.setPythonTag("velocity", 0)

    def updateSmileys(self, task):
        for smiley in self.smRoot.findAllMatches("smiley.egg"):
            vel = smiley.getPythonTag("velocity")
            z = smiley.getZ()
            if z <= 0:
                vel = random.uniform(0.1, 0.8)
            smiley.setZ(z + vel)
            vel -= 0.01
            smiley.setPythonTag("velocity", vel)
        return task.cont

    def addEnvironment(self, parent):
        env = loader.loadModel("environment")
        env.reparentTo(parent)
        env.setScale(0.01, 0.01, 0.01)
        env.setPos(render, random.uniform(-20, 20), random.uniform(-30, 30), random.uniform(0, 30))