from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec4

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.pandaActor = Actor("panda", {"walk": "panda-walk"})
        self.pandaActor.reparentTo(render)
        self.pandaActor.loop("walk")

        self.cam.node().getDisplayRegion(0).setActive(0)

        cameras = [self.makeCamera(self.win), self.makeCamera(self.win)]
        self.makeRegion(cameras[0], Vec4(0, 0.5, 0, 1), Vec4(0, 1, 0, 1))
        self.makeRegion(cameras[1], Vec4(0.5, 1, 0, 1), Vec4(1, 0, 0, 1))

        cameras[0].setPos(0, -30, 6)
        cameras[1].setPos(-30, 0, 6)
        cameras[1].lookAt(0, 0, 6)

    def makeRegion(self, cam, dimensions, color):
        region = cam.node().getDisplayRegion(0)
        region.setDimensions(dimensions.getX(), dimensions.getY(), dimensions.getZ(), dimensions.getW())
        region.setClearColor(color)
        region.setClearColorActive(True)
        aspect = float(region.getPixelWidth()) / float(region.getPixelHeight())
        cam.node().getLens().setAspectRatio(aspect)
