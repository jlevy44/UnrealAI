from xml.etree.ElementTree import *
from direct.gui.DirectGui import *
from panda3d.core import *

class GuiHandler:
    def __init__(self):
        self.controls = {}

def GuiFromXml(fname, handler):
    elements = ElementTree()
    elements.parse(fname)

    handleButtons(elements, handler)
    handleLabels(elements, handler)
    handleEntries(elements, handler)
    handleRadioGroups(elements, handler)

def handleButtons(elements, handler):
    buttons = elements.findall("button")
    for button in buttons:
        createButton(button, handler)

def handleLabels(elements, handler):
    labels = elements.findall("label")
    for label in labels:
        createLabel(label, handler)

def handleEntries(elements, handler):
    entries = elements.findall("entry")
    for entry in entries:
        createEntry(entry, handler)

def handleRadioGroups(elements, handler):
    rdoGroups = elements.findall("radiogroup")
    for group in rdoGroups:
        handleRadios(group, handler)

def handleRadios(elements, handler):
    radios = elements.findall("radio")
    created = []
    for radio in radios:
        created.append(createRadio(radio, handler))
    for btn in created:
        btn.setOthers(created)

def getParams(element):
    params = {}
    params["scale"] = float(element.findtext("scale", 1))
    params["text"] = element.findtext("text", "")
    params["mayChange"] = int(element.findtext("mayChange", 0))
    params["width"] = float(element.findtext("width", 1))
    params["value"] = [int(element.findtext("value", 0))]    
    params["variable"] = element.findtext("variable", "")
    params["name"] = element.findtext("name", "")
    params["command"] = element.findtext("command", "")
    
    fcolorElem = element.find("frameColor")
    if fcolorElem != None:
        r = fcolorElem.get("r", 0)
        g = fcolorElem.get("g", 0)
        b = fcolorElem.get("b", 0)
        a = fcolorElem.get("a", 0)
        color = Vec4(float(r), float(g), float(b), float(a))
        params["frameColor"] = color
    else:
        color = Vec4(0, 0, 0, 0)
        params["frameColor"] = color
        
    posElem = element.find("pos")
    if posElem != None:
        x = posElem.get("x", 0)
        y = posElem.get("y", 0)
        z = posElem.get("z", 0)
        pos = Vec3(float(x), float(y), float(z))
        params["pos"] = pos
    else:
        pos = Vec3(0, 0, 0)
        params["pos"] = pos

    return params

def createButton(element, handler):
    params = getParams(element)
    assert params["command"] != ""
    assert params["name"] != ""
    button = DirectButton(text = params["text"],
                          scale = params["scale"], 
                          command = getattr(handler, params["command"]), 
                          pos = params["pos"])
    handler.controls[params["name"]] = button

def createLabel(element, handler):
    params = getParams(element)
    assert params["name"] != ""
    label = DirectLabel(text = params["text"], 
                        pos = params["pos"], 
                        scale = params["scale"],
                        textMayChange = params["mayChange"],
                        frameColor = params["frameColor"])
    handler.controls[params["name"]] = label

def createEntry(element, handler):
    params = getParams(element)
    assert params["name"] != ""
    entry = DirectEntry(scale = params["scale"],
                        pos = params["pos"],
                        width = params["width"])
    handler.controls[params["name"]] = entry

def createRadio(element, handler):
    params = getParams(element)
    assert params["variable"] != ""
    assert params["name"] != ""
    radio = DirectRadioButton(text = params["text"], 
                              variable = getattr(handler, params["variable"]), 
                              value = params["value"], 
                              scale = params["scale"],
                              pos = params["pos"])
    handler.controls[params["name"]] = radio
    return radio
