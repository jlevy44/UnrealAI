from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.interval.IntervalGlobal import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.loop("walk")

        cm = CardMaker("plane")
        cm.setFrame(-10, 10, -10, 10)
        plane = render.attachNewNode(cm.generate())
        plane.setP(270)
        
        self.cam.setPos(0, -40, 6)

        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.3, 0.2, 0.2, 1.0))
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)

        dirLight = DirectionalLight("directional")
        dirLight.setColor(Vec4(0.3, 0.9, 0.3, 1.0))
        dirNode = render.attachNewNode(dirLight)
        dirNode.setHpr(60, 0, 90)
        render.setLight(dirNode)

        pntLight = PointLight("point")
        pntLight.setColor(Vec4(3.9, 3.9, 3.8, 1.0))
        pntNode = render.attachNewNode(pntLight)
        pntNode.setPos(0, 0, 15)
        self.panda.setLight(pntNode)

        sptLight = Spotlight("spot")
        sptLens = PerspectiveLens()
        sptLight.setLens(sptLens)
        sptLight.setColor(Vec4(1.0, 0.4, 0.4, 1.0))
        sptLight.setShadowCaster(True)
        sptNode = render.attachNewNode(sptLight)
        sptNode.setPos(-10, -10, 20)
        sptNode.lookAt(self.panda)
        render.setLight(sptNode)

        render.setShaderAuto()

        self.activeRamp = 0
        toggle = Func(self.toggleRamp)
        switcher = Sequence(toggle, Wait(3))
        switcher.loop()

    def toggleRamp(self):
        if self.activeRamp == 0:
            render.setAttrib(LightRampAttrib.makeDefault())
        elif self.activeRamp == 1:
            render.setAttrib(LightRampAttrib.makeHdr0())
        elif self.activeRamp == 2:
            render.setAttrib(LightRampAttrib.makeHdr1())
        elif self.activeRamp == 3:
            render.setAttrib(LightRampAttrib.makeHdr2())
        elif self.activeRamp == 4:
            render.setAttrib(LightRampAttrib.makeSingleThreshold(0.1, 0.3))
        elif self.activeRamp == 5:
            render.setAttrib(LightRampAttrib.makeDoubleThreshold(0, 0.1, 0.3, 0.8))

        self.activeRamp += 1
        if self.activeRamp > 5:
            self.activeRamp = 0
