from panda3d.bullet import BulletVehicle, BulletBoxShape, BulletRigidBodyNode
from direct.gui.DirectGui import *
from panda3d.core import Vec3, Point3
class Car:
    def __init__(self):
        # Chassis body
        self.shape = BulletBoxShape(Vec3(0.7, 1.5, 0.5))
