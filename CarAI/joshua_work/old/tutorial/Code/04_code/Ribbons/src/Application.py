from direct.showbase.ShowBase import ShowBase
from direct.showbase.RandomNumGen import RandomNumGen
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from Ribbon import Ribbon

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.loop("walk")
        self.panda.setHpr(-90, 0, 0)

        self.ribbon = Ribbon(self.panda, Vec4(1, 1, 1, 1), 3, 10, 0.3)
        self.ribbon.getRoot().setZ(5)
                
        self.walkIval1 = self.panda.posInterval(1, Vec3(-12, 0, 0), startPos = Vec3(12, 0, 0))
        self.walkIval2 = self.panda.posInterval(1, Vec3(12, 0, 0), startPos = Vec3(-12, 0, 0))
        self.turnIval1 = self.panda.hprInterval(0.1, Vec3(90, 0, 0), startHpr = Vec3(-90, 0, 0))
        self.turnIval2 = self.panda.hprInterval(0.1, Vec3(-90, 0, 0), startHpr = Vec3(90, 0, 0))
        self.pandaWalk = Sequence(self.walkIval1, self.turnIval1, self.walkIval2, self.turnIval2)
        self.pandaWalk.loop()

        self.cam.setPos(0, -60, 6)
        self.cam.lookAt(0, 0, 6);
