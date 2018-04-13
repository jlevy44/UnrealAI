from direct.showbase.DirectObject import DirectObject
from panda3d.core import *

class InputRecorder(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.events = []        
        self.setupEvents()

    def setupEvents(self):
        self.startTime = globalClock.getFrameTime()
        del self.events[:]
        self.accept("walk-start", self.recordEvent, ["walk-start"])
        self.accept("walk-stop", self.recordEvent, ["walk-stop"])
        self.accept("reverse-start", self.recordEvent, ["reverse-start"])
        self.accept("reverse-stop", self.recordEvent, ["reverse-stop"])
        self.accept("walk", self.recordEvent, ["walk"])
        self.accept("reverse", self.recordEvent, ["reverse"])        
        self.accept("turn", self.recordEvent, ["turn"])

    def replay(self):
        self.ignoreAll()
        self.acceptOnce("replay-done", self.setupEvents)
        last = 0
        for e in self.events:
            taskMgr.doMethodLater(e[0], self.createInput, "replay", extraArgs = [e[1], e[2]])
            last = e[0]
        taskMgr.doMethodLater(last + 1, messenger.send, "replay done", extraArgs = ["replay-done"])

    def recordEvent(self, name, rate = 0):
        self.events.append((globalClock.getFrameTime() - self.startTime, name, rate))
        
    def createInput(self, event, rate):
        if not event in ["walk", "reverse", "turn"]:
            messenger.send(event)
        else:
            messenger.send(event, [rate])
