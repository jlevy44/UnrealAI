from direct.showbase.ShowBase import ShowBase
from direct.showbase.RandomNumGen import RandomNumGen
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from direct.interval.IntervalGlobal import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.setHpr(-90, 0, 0)

        self.walkIval1 = self.panda.posInterval(2, Vec3(-8, 0, 0), startPos = Vec3(8, 0, 0))
        self.walkIval2 = self.panda.posInterval(2, Vec3(8, 0, 0), startPos = Vec3(-8, 0, 0))
        self.turnIval1 = self.panda.hprInterval(0.5, Vec3(90, 0, 0), startHpr = Vec3(-90, 0, 0))
        self.turnIval2 = self.panda.hprInterval(0.5, Vec3(-90, 0, 0), startHpr = Vec3(90, 0, 0))
        self.colorIval = Func(self.randomColor)
        self.pandaAnim = ActorInterval(self.panda, "walk", loop = 1, duration = 5)
        self.pandaMove = Sequence(self.walkIval1, self.turnIval1, self.colorIval, self.walkIval2, self.turnIval2, self.colorIval)
        self.pandaWalk = Parallel(self.pandaAnim, self.pandaMove)
        self.pandaWalk.loop()

        self.cam.setPos(0, -50, 6)

    def randomColor(self):
        rand = RandomNumGen(globalClock.getFrameTime())
        self.panda.setColorScale(rand.random(), rand.random(), rand.random(), 1)
