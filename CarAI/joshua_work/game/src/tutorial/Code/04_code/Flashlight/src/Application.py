from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.world = loader.loadModel("environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        self.proj = render.attachNewNode(LensNode("proj"))
        lens = PerspectiveLens()
        self.proj.node().setLens(lens)
        self.proj.reparentTo(self.cam)
        self.proj.setHpr(0, -5, 0)
        self.proj.setPos(0, 10, 0)

        tex = loader.loadTexture("flashlight.png")
        tex.setWrapU(Texture.WMClamp)
        tex.setWrapV(Texture.WMClamp)
        ts = TextureStage('ts')
        self.world.projectTexture(ts, tex, self.proj)

        self.cam.setPos(0, -10, 10)
