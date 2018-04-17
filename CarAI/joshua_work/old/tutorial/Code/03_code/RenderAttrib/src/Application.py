from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import loadPrcFileData

loadPrcFileData("", "multisamples 8")

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.pandas = []

        for i in range(4):
            panda = Actor("panda", {"walk": "panda-walk"})
            panda.reparentTo(render)
            panda.loop("walk")
            panda.setX(-10.5 + i * 7)
            self.pandas.append(panda)

        render.setAntialias(AntialiasAttrib.MAuto)

        mask = ColorWriteAttrib.CRed
        mask |= ColorWriteAttrib.CBlue
        mask |= ColorWriteAttrib.CAlpha
        self.pandas[0].setAttrib(ColorWriteAttrib.make(mask))
        self.pandas[1].setRenderMode(RenderModeAttrib.MWireframe, 1)
        self.pandas[2].setColorScale(0.5, 0.5, 0.5, 0.5)
        self.pandas[3].setColor(0.5, 0.5, 0.5, 0.5)

        self.smiley = loader.loadModel("smiley")
        self.smiley.reparentTo(render)
        self.smiley.setDepthWrite(False)
        self.smiley.setDepthTest(False)
        self.smiley.setPos(5, 20, 3)
        self.smiley.setScale(3)
        
        self.cam.setPos(0, -40, 6)
