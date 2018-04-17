from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.physics import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.enableParticles()

        particles = Particles()
        particles.setPoolSize(1000)
        particles.setBirthRate(0.1)
        particles.setLitterSize(10)
        particles.setLitterSpread(3)
        particles.setFactory("PointParticleFactory")
        particles.setRenderer("GeomParticleRenderer")
        particles.setEmitter("SphereVolumeEmitter")

        smiley = loader.loadModel("smiley")
        smiley.setScale(0.1)
        particles.getRenderer().setGeomNode(smiley.node())
        particles.enable()

        self.effect = ParticleEffect("peffect", particles)
        self.effect.reparentTo(render)
        self.effect.enable()
        
        self.cam.setPos(0, -10, 0)

        #self.effect.saveConfig("particles.ptf")        
