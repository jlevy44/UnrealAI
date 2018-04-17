from direct.showbase.DirectObject import DirectObject

def handle_event(event):
    def inner_event(func):
        func.event_name = event
        return func
    return inner_event

class GameObject(DirectObject):
    def __init__(self):
        for attrib in dir(self):
            method = getattr(self, attrib)
            if callable(method) and hasattr(method, 'event_name'):
                self.accept(method.event_name, method)

    def destroy(self):
        self.ignoreAll()