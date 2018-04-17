from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.world = loader.loadModel("environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        shader = loader.loadShader("shader.cg")
        render.setShader(shader)

        self.cam.setPos(0, -40, 10)
