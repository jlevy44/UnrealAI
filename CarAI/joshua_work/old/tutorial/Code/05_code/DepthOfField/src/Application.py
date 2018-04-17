from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.filter.FilterManager import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupScene()
        self.setupLight()
        self.setupPostFx()

    def setupScene(self):
        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.loop("walk")

        smiley = loader.loadModel("smiley")
        smiley.reparentTo(render)
        smiley.setPos(5, -15, 10)

        smiley = loader.loadModel("smiley")
        smiley.reparentTo(render)
        smiley.setPos(5, 0, 10)

        smiley = loader.loadModel("smiley")
        smiley.reparentTo(render)
        smiley.setPos(5, 20, 10)

        self.world = loader.loadModel("environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)
        
        self.cam.setPos(0, -40, 6)
        self.cam.node().getLens().setNearFar(1.0, 300.0)

    def setupLight(self):
        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.2, 0.1, 0.1, 1.0))
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)

        dirLight = DirectionalLight("directional")
        dirLight.setColor(Vec4(0.1, 0.4, 0.1, 1.0))
        dirNode = render.attachNewNode(dirLight)
        dirNode.setHpr(60, 0, 90)
        render.setLight(dirNode)

        pntLight = PointLight("point")
        pntLight.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
        pntNode = render.attachNewNode(pntLight)
        pntNode.setPos(0, 0, 15)
        self.panda.setLight(pntNode)

        sptLight = Spotlight("spot")
        sptLens = PerspectiveLens()
        sptLight.setLens(sptLens)
        sptLight.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        sptLight.setShadowCaster(True)
        sptNode = render.attachNewNode(sptLight)
        sptNode.setPos(-10, -10, 50)
        sptNode.lookAt(self.panda)
        render.setLight(sptNode)

        render.setShaderAuto()

    def setupPostFx(self):
        self.filterMan = FilterManager(self.win, self.cam)

        colorTex = Texture()
        blurTex = Texture()
        depthTex = Texture()

        finalQuad = self.filterMan.renderSceneInto(colortex = colorTex, depthtex = depthTex)
        blurQuad = self.filterMan.renderQuadInto(colortex = blurTex, div = 4)
        blurQuad.setShader(loader.loadShader("blur.cg"))
        blurQuad.setShaderInput("color", colorTex)

        finalQuad.setShader(loader.loadShader("depth.cg"))
        finalQuad.setShaderInput("color", colorTex)
        finalQuad.setShaderInput("blur", blurTex)
        finalQuad.setShaderInput("depth", depthTex) 
