from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        cm = CardMaker("plane")
        cm.setFrame(-3, 3, -3, 3)
        
        self.plane = render.attachNewNode(cm.generate())
        tex = loader.loadTexture("texture.png")
        self.plane.setTexture(tex)

        self.cam.setPos(0, -12, 0)
        taskMgr.add(self.animate, "texanim")

    def animate(self, task):
        texStage = TextureStage.getDefault()

        offset = self.plane.getTexOffset(texStage)
        offset.setY(offset.getY() - 0.005)
        self.plane.setTexOffset(texStage, offset)

        scale = sin(offset.getY()) * 2
        self.plane.setTexScale(texStage, scale, scale)

        rotate = sin(offset.getY()) * 80
        self.plane.setTexRotate(texStage, rotate)
        return task.cont
