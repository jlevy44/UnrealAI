from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from direct.interval.IntervalGlobal import *
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
        self.panda.setHpr(270, 0, 0)
        self.panda.loop("walk")

        self.walkIval1 = self.panda.posInterval(2, Vec3(-8, -8, 0), startPos = Vec3(8, -8, 0))
        self.walkIval2 = self.panda.posInterval(2, Vec3(-8, 8, 0), startPos = Vec3(-8, -8, 0))
        self.walkIval3 = self.panda.posInterval(2, Vec3(8, 8, 0), startPos = Vec3(-8, 8, 0))
        self.walkIval4 = self.panda.posInterval(2, Vec3(8, -8, 0), startPos = Vec3(8, 8, 0))

        self.turnIval1 = self.panda.hprInterval(0.5, Vec3(180, 0, 0), startHpr = Vec3(270, 0, 0))
        self.turnIval2 = self.panda.hprInterval(0.5, Vec3(90, 0, 0), startHpr = Vec3(180, 0, 0))
        self.turnIval3 = self.panda.hprInterval(0.5, Vec3(0, 0, 0), startHpr = Vec3(90, 0, 0))
        self.turnIval4 = self.panda.hprInterval(0.5, Vec3(-90, 0, 0), startHpr = Vec3(0, 0, 0))

        self.pandaWalk = Sequence(self.walkIval1, self.turnIval1, 
                                  self.walkIval2, self.turnIval2,
                                  self.walkIval3, self.turnIval3,
                                  self.walkIval4, self.turnIval4)
        self.pandaWalk.loop()
        self.followCam = FollowCam(self.cam, self.panda)
