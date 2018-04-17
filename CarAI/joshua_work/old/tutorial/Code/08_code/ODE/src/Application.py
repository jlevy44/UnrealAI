from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.ode import *
import random

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.smiley = loader.loadModel("smiley")
        self.smileyCount = 0
        self.cam.setPos(0, -100, 10)

        self.setupODE()
        self.addGround()

        taskMgr.doMethodLater(0.01, self.addSmiley, "AddSmiley")
        taskMgr.add(self.updateODE, "UpdateODE")      

    def setupODE(self):
        self.odeWorld = OdeWorld()
        self.odeWorld.setGravity(0, 0, -9.81)
        self.odeWorld.initSurfaceTable(1)
        self.odeWorld.setSurfaceEntry(0, 0, 200, 0.7, 0.2, 0.9, 0.00001, 0.0, 0.002)

        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.odeWorld)
        self.contacts = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contacts)

    def addGround(self):
        cm = CardMaker("ground")
        cm.setFrame(-500, 500, -500, 500)
        ground = render.attachNewNode(cm.generate())
        ground.setColor(0.2, 0.4, 0.8)
        ground.lookAt(0, 0, -1)
        groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))        

    def addSmiley(self, task):
        sm = render.attachNewNode("smiley-instance")
        sm.setPos(random.uniform(-20, 20), random.uniform(-30, 30), random.uniform(10, 30))
        self.smiley.instanceTo(sm)

        body = OdeBody(self.odeWorld)
        mass = OdeMass()
        mass.setSphereTotal(10, 1)
        body.setMass(mass)
        body.setPosition(sm.getPos())
        geom = OdeSphereGeom(self.space, 1)
        geom.setBody(body)

        sm.setPythonTag("body", body)
        self.smileyCount += 1

        if self.smileyCount == 1000:
            return task.done

        return task.again

    def updateODE(self, task):
        self.space.autoCollide()
        self.odeWorld.quickStep(globalClock.getDt())

        for smiley in render.findAllMatches("smiley-instance"):
            body = smiley.getPythonTag("body")
            smiley.setPosQuat(body.getPosition(), Quat(body.getQuaternion()))

        self.contacts.empty()
        return task.cont
