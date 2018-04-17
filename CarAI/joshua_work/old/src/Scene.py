from direct.gui.DirectGui import *
from panda3d.core import DirectionalLight, AmbientLight, VBase4, Vec3
from panda3d.bullet import BulletWorld

class Scene:

    def __init__(self):
        self.scene = BulletWorld()
        self.scene.setGravity(Vec3(0, 0, -9.81))
        base.setBackgroundColor(0.6,0.9,0.9)

        # sun light
        self.sun = DirectionalLight("The Sun")
        self.sun_np = render.attachNewNode(self.sun)
        self.sun_np.setHpr(0,-60,0)
        render.setLight(self.sun_np)

        # ambient setLight
        self.amb = AmbientLight("The Ambient Light")
        self.amb.setColor(VBase4(0.39,0.39,0.39, 1))
        self.amb_np = render.attachNewNode(self.amb)
        render.setLight(self.amb_np)

        
