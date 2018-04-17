from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.physx import *
import random

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.smiley = loader.loadModel("smiley")
        self.smileyCount = 0
        self.cam.setPos(0, -100, 10)

        self.setupPhysX()
        self.addGround()

        taskMgr.doMethodLater(0.01, self.addSmiley, "AddSmiley")
        taskMgr.add(self.updatePhysX, "UpdatePhysX")

    def setupPhysX(self):
        scene = PhysxSceneDesc()
        scene.setGravity(Vec3(0, 0, -9.81))
        self.physxScene = PhysxManager.getGlobalPtr().createScene(scene)

        mat = self.physxScene.getMaterial(0)
        mat.setRestitution(0.7)
        mat.setStaticFriction(0.5)
        mat.setDynamicFriction(0.8)

    def addGround(self):
        cm = CardMaker("ground")
        cm.setFrame(-500, 500, -500, 500)
        ground = render.attachNewNode(cm.generate())
        ground.setColor(0.2, 0.4, 0.8)
        ground.lookAt(0, 0, -1)

        shape = PhysxPlaneShapeDesc()
        shape.setPlane(Vec3(0, 0, 1), 0)
        actor = PhysxActorDesc()
        actor.addShape(shape)
        self.physxScene.createActor(actor)

    def addSmiley(self, task):
        sm = render.attachNewNode("smiley-instance")
        self.smiley.instanceTo(sm)

        shape = PhysxSphereShapeDesc()
        shape.setRadius(1)
        body = PhysxBodyDesc()
        body.setMass(10)
        actor = PhysxActorDesc()
        actor.setBody(body)
        actor.addShape(shape)
        actor.setGlobalPos(Point3(random.uniform(-20, 20), random.uniform(-30, 30), random.uniform(10, 30)))
        physxActor = self.physxScene.createActor(actor)
        physxActor.attachNodePath(sm)

        self.smileyCount += 1

        if self.smileyCount == 1000:
            return task.done

        return task.again

    def updatePhysX(self, task):
        self.physxScene.simulate(globalClock.getDt())
        self.physxScene.fetchResults()
        return task.cont
