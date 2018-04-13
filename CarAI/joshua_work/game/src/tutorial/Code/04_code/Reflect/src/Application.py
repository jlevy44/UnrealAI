from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.interval.IntervalGlobal import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.world = loader.loadModel("environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        self.teapot = loader.loadModel("teapot")
        self.teapot.reparentTo(render)
        self.teapot.setPos(0, 0, 10)

        cubeCams = NodePath("cubeCams")
        cubeBuffer = self.win.makeCubeMap("cubemap", 128, cubeCams)
        cubeCams.reparentTo(self.teapot)

        tex = TextureStage.getDefault()
        self.teapot.setTexGen(tex, TexGenAttrib.MWorldCubeMap)
        self.teapot.setTexture(cubeBuffer.getTexture())

        rotate = self.teapot.hprInterval(10, Vec3(360, 0, 0), startHpr = Vec3(0, 0, 0))
        move = self.teapot.posInterval(10, Vec3(-10, 0, 10), startPos = Vec3(10, 0, 10))
        rotate.loop()
        move.loop()

        self.cam.setPos(0, -30, 10)
