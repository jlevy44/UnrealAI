from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import random

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(0, -50, 10)
        self.setupCD()
        self.addSmiley()
        self.addFloor()
        taskMgr.add(self.updateSmiley, "UpdateSmiley")

    def setupCD(self):
        base.cTrav = CollisionTraverser()
        base.cTrav.showCollisions(render)
        self.notifier = CollisionHandlerEvent()
        self.notifier.addInPattern("%fn-in-%in")
        self.accept("frowney-in-floor", self.onCollision)

    def addSmiley(self):
        self.frowney = loader.loadModel("frowney")
        self.frowney.reparentTo(render)
        self.frowney.setPos(0, 0, 10)            
        self.frowney.setPythonTag("velocity", 0)

        col = self.frowney.attachNewNode(CollisionNode("frowney"))
        col.node().addSolid(CollisionSphere(0, 0, 0, 1.1))
        col.show()
        base.cTrav.addCollider(col, self.notifier)

    def addFloor(self):
        floor = render.attachNewNode(CollisionNode("floor"))
        floor.node().addSolid(CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0))))
        floor.show()

    def onCollision(self, entry):
        vel = random.uniform(0.1, 0.8)
        self.frowney.setPythonTag("velocity", vel)        

    def updateSmiley(self, task):
        vel = self.frowney.getPythonTag("velocity")
        z = self.frowney.getZ()
        self.frowney.setZ(z + vel)
        vel -= 0.01
        self.frowney.setPythonTag("velocity", vel)
        return task.cont
