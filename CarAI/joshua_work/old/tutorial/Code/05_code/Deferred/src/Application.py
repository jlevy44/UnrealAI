from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.filter.FilterManager import *
import random

loadPrcFileData('', 'show-buffers 1')

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupScene()
        self.setupLight()
        self.setupCams()
        self.setupPostFx()

    def setupScene(self):
        self.scene = render.attachNewNode("scene")
        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(self.scene)
        self.panda.loop("walk")

        self.world = loader.loadModel("environment")
        self.world.reparentTo(self.scene)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        self.scene.setShaderAuto()
        
    def setupCams(self):
        self.lightCam = self.makeCamera(self.win)
        self.lightCam.reparentTo(self.cam)

        sceneMask = BitMask32(1)
        lightMask = BitMask32(2)
        self.cam.node().setCameraMask(sceneMask)
        self.lightCam.node().setCameraMask(lightMask)
        self.lights.hide(sceneMask)
        self.ambient.hide(sceneMask)
        self.scene.hide(lightMask)

        self.cam.node().getDisplayRegion(0).setSort(1)
        self.lightCam.node().getDisplayRegion(0).setSort(2)
        self.win.setSort(3)

        self.lightCam.node().getDisplayRegion(0).setClearColor(Vec4(0, 0, 0, 1))
        self.lightCam.node().getDisplayRegion(0).setClearColorActive(1)

        self.cam.setPos(0, -40, 6)

    def setupLight(self):
        self.lights = render.attachNewNode("lights")
        self.sphere = loader.loadModel("misc/sphere")
        
        for i in range(400):
            light = self.lights.attachNewNode("light")
            light.setPos(random.uniform(-15, 15), random.uniform(-5, 50), random.uniform(0, 15))
            light.setColor(random.random(), random.random(), random.random())
            light.setScale(5)
            self.sphere.instanceTo(light)
            
            vlight = self.scene.attachNewNode("vlight")
            vlight.setPos(light.getPos())
            vlight.setColor(light.getColor())
            vlight.setScale(0.1)
            self.sphere.instanceTo(vlight)

        cm = CardMaker("ambient")
        cm.setFrame(-100, 100, -100, 100)
        self.ambient = render.attachNewNode("ambient")
        self.ambient.attachNewNode(cm.generate())
        self.ambient.setColor(0.1, 0.1, 0.1, 1)
        self.ambient.reparentTo(self.cam)
        self.ambient.setPos(0, 5, 0)

    def setupPostFx(self):
        self.gbufMan = FilterManager(self.win, self.cam)
        self.lightMan = FilterManager(self.win, self.lightCam)
        
        albedo = Texture()
        depth = Texture()
        normal = Texture()
        final = Texture()

        self.gbufMan.renderSceneInto(colortex = albedo, depthtex = depth, auxtex = normal, auxbits = AuxBitplaneAttrib.ABOAuxNormal)
        
        lightQuad = self.lightMan.renderSceneInto(colortex = final)
        lightQuad.setShader(loader.loadShader("pass.cg"))
        lightQuad.setShaderInput("color", final)

        self.ambient.setShader(loader.loadShader("ambient.cg"))
        self.ambient.setShaderInput("albedo", albedo)

        self.ambient.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOne))
        self.ambient.setAttrib(DepthWriteAttrib.make(DepthWriteAttrib.MOff))

        self.lights.setShader(loader.loadShader("light.cg"))
        self.lights.setShaderInput("albedo", albedo)
        self.lights.setShaderInput("depth", depth)
        self.lights.setShaderInput("normal", normal)

        self.lights.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOne))
        self.lights.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
        self.lights.setAttrib(DepthWriteAttrib.make(DepthWriteAttrib.MOff))
