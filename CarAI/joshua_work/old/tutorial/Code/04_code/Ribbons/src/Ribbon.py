from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *

class RibbonNode():
    def __init__(self, pos, damping):
        self.pos = Vec3(pos)
        self.damping = damping
        self.delta = Vec3()

    def update(self, pos):
        self.delta = (pos - self.pos) * self.damping
        self.pos += self.delta


class Ribbon():
    def __init__(self, parent, color, thickness, length, damping):
        
        self.parent = parent
        self.length = length
        self.thickness = thickness
        self.color = color

        self.lineGen = MeshDrawer()
        self.lineGen.setBudget(100)
        genNode = self.lineGen.getRoot()
        genNode.reparentTo(render)
        genNode.setTwoSided(True)
        genNode.setTransparency(True)

        pos = parent.getPos(render)

        self.trailPoints = []
        for i in range(length):
            self.trailPoints.append(RibbonNode(pos, damping))

        taskMgr.add(self.trail, "update trail")

    def getRoot(self):
        return self.lineGen.getRoot()
        
    def trail(self, task):
        pos = self.parent.getPos(render)
        self.trailPoints[0].update(pos)

        for i in range(1, self.length):
            self.trailPoints[i].update(self.trailPoints[i - 1].pos)

        self.lineGen.begin(base.cam, render)
        color = Vec4(self.color)
        thickness = self.thickness

        for i in range(self.length - 1):
            p1 = self.trailPoints[i].pos
            p2 = self.trailPoints[i + 1].pos

            startColor = Vec4(color)
            endColor = Vec4(color)
            endColor.setW(color.getW() - 0.2)
            color = Vec4(endColor)
            self.lineGen.unevenSegment(p1, p2, 0, thickness, startColor, thickness - 0.3, endColor)
            thickness -= 0.3

        self.lineGen.end()
        return task.cont
