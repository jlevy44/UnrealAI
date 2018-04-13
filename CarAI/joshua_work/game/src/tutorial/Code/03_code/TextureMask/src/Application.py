from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.box = self.buildCube(2)
        tex = loader.loadTexture("texture.png", "mask.png")
        self.box.setTexture(tex)
        self.box.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.box.setTwoSided(1)
        self.cam.setPos(10, -10, 10)
        self.cam.lookAt(0, 0, 0)

    def buildCube(self, size):
        center = render.attachNewNode("cubeCenter")
        cm = CardMaker("plane")
        cm.setFrame(-size, size, -size, size)
        front = center.attachNewNode(cm.generate())
        front.setY(-size)
        back = center.attachNewNode(cm.generate())
        back.setY(size)
        back.setH(180)
        left = center.attachNewNode(cm.generate())
        left.setX(-size)
        left.setH(270)
        right = center.attachNewNode(cm.generate())
        right.setX(size)
        right.setH(90)
        top = center.attachNewNode(cm.generate())
        top.setZ(size)
        top.setP(270)
        btm = center.attachNewNode(cm.generate())
        btm.setZ(-size)
        btm.setP(90)
        return center
