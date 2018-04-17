from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3

class FollowCam():
    def __init__(self, camera, target):
        self.dummy = render.attachNewNode("cam" + target.getName())
        self.turnRate = 2.2
        self.camera = camera
        self.target = target
        taskMgr.add(self.updateCamera, "updateCamera" + target.getName())

    def updateCamera(self, task):
        self.dummy.setPos(self.target.getPos())
        heading = self.clampAngle(self.dummy.getH())

        turnDiff = self.target.getH() - heading
        turnDiff = self.clampAngle(turnDiff)

        dt = globalClock.getDt()
        turn = turnDiff * dt
        self.dummy.setH(heading + turn * self.turnRate)

        self.camera.setPos(self.dummy.getPos())
        self.camera.setY(self.dummy, 40)
        self.camera.setZ(self.dummy, 10)
        self.camera.lookAt(self.target.getPos() + Vec3(0, 0, 7))

        return task.cont

    def clampAngle(self, angle):
        while angle < -180:
            angle = angle + 360

        while angle > 180:
            angle = angle - 360

        return angle
