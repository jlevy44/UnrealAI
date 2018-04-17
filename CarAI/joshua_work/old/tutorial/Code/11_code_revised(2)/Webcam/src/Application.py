from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.vision import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        for i in range(WebcamVideo.getNumOptions()):
            print WebcamVideo.getOption(i)

        if WebcamVideo.getNumOptions() > 0:
            opt = WebcamVideo.getOption(0)
            self.cursor = opt.open()
            self.tex = Texture()
            self.cursor.setupTexture(self.tex)

            cm = CardMaker("plane")
            cm.setFrame(-1, 1, -1, 1)
            plane = render2d.attachNewNode(cm.generate())
            plane.setTexture(self.tex)

            scaleX = float(self.cursor.sizeX()) / float(self.tex.getXSize())
            scaleY = float(self.cursor.sizeY()) / float(self.tex.getYSize())
            plane.setTexScale(TextureStage.getDefault(), Vec2(scaleX, scaleY))

            taskMgr.add(self.update, "update video")

    def update(self, task):
        if self.cursor.ready():
            self.cursor.fetchIntoTexture(0, self.tex, 0)
        return task.cont
