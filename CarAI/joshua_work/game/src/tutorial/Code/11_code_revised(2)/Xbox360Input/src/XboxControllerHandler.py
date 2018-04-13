from InputHandler import InputHandler
from panda3d.core import *
import pygame
import math

class XboxControllerState:
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    BACK = 6
    START = 7
    LS = 8
    RS = 9

    def __init__(self, joy):
        self.joy = joy
        self.leftStick = Vec2()
        self.rightStick = Vec2()
        self.dpad = Vec2()
        self.triggers = 0.0
        self.buttons = [False] * self.joy.get_numbuttons()

    def update(self):
        self.leftStick.setX(self.joy.get_axis(0))
        self.leftStick.setY(self.joy.get_axis(1))
        self.rightStick.setX(self.joy.get_axis(4))
        self.rightStick.setY(self.joy.get_axis(3))
        self.triggers = self.joy.get_axis(2)

        for i in range(self.joy.get_numbuttons()):
            self.buttons[i] = self.joy.get_button(i)

class XboxControllerHandler(InputHandler):
    def __init__(self):
        InputHandler.__init__(self)

        self.wasWalking = False
        self.wasReversing = False
        self.controller = None

        pygame.init()
        pygame.joystick.init()

        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            name = joy.get_name()
    
            if "Xbox 360" in name or "XBOX 360" in name:
                joy.init()
                self.controller = joy
                self.state = XboxControllerState(joy)

        taskMgr.add(self.updateInput, "update input")

    def updateInput(self, task):
        pygame.event.pump()

        if self.controller:
            self.state.update()

        x = self.state.rightStick.getX()
        y = self.state.leftStick.getY()

        if y < -0.5 and not self.wasWalking:
            self.wasWalking = True
            self.beginWalk()
        elif not y < -0.5 and self.wasWalking:
            self.wasWalking = False
            self.endWalk()
        elif y > 0.5 and not self.wasReversing:
            self.wasReversing = True
            self.beginReverse()
        elif not y > 0.5 and self.wasReversing:
            self.wasReversing = False
            self.endReverse()

        if math.fabs(x) > 0.2:
            messenger.send("turn", [-x])

        self.dispatchMessages()
        return task.cont
