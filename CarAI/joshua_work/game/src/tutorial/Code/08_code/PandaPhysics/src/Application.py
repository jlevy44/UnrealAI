from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.physics import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(0, -50, 10)
        self.setupCD()
        self.setupPhysics()
        self.addSmiley()
        self.addFloor()

    def setupCD(self):
        base.cTrav = CollisionTraverser()
        base.cTrav.showCollisions(render)
        self.notifier = CollisionHandlerEvent()
        self.notifier.addInPattern("%fn-in-%in")
        self.notifier.addOutPattern("%fn-out-%in")
        self.accept("smiley-in-floor", self.onCollisionStart)
        self.accept("smiley-out-floor", self.onCollisionEnd)

    def setupPhysics(self):
        base.enableParticles()
        gravNode = ForceNode("gravity")
        render.attachNewNode(gravNode)
        gravityForce = LinearVectorForce(0, 0, -9.81)
        gravNode.addForce(gravityForce)
        base.physicsMgr.addLinearForce(gravityForce)

    def addSmiley(self):
        actor = ActorNode("physics")
        actor.getPhysicsObject().setMass(10)
        self.phys = render.attachNewNode(actor)
        base.physicsMgr.attachPhysicalNode(actor)

        self.smiley = loader.loadModel("smiley")
        self.smiley.reparentTo(self.phys)
        self.phys.setPos(0, 0, 10)

        thrustNode = ForceNode("thrust")
        self.phys.attachNewNode(thrustNode)
        self.thrustForce = LinearVectorForce(0, 0, 400)
        self.thrustForce.setMassDependent(1)
        thrustNode.addForce(self.thrustForce)

        col = self.smiley.attachNewNode(CollisionNode("smiley"))
        col.node().addSolid(CollisionSphere(0, 0, 0, 1.1))
        col.show()
        base.cTrav.addCollider(col, self.notifier)

    def addFloor(self):
        floor = render.attachNewNode(CollisionNode("floor"))
        floor.node().addSolid(CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0))))
        floor.show()

    def onCollisionStart(self, entry):
        base.physicsMgr.addLinearForce(self.thrustForce)

    def onCollisionEnd(self, entry):
        base.physicsMgr.removeLinearForce(self.thrustForce)
