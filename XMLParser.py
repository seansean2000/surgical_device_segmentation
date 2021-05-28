import xml.dom.minidom

def handleXmlAnnotation(xmlAnnotationPath):
    doc = xml.dom.minidom.parse(xmlAnnotationPath)
    objDics = []
    for obj in doc.getElementsByTagName("object"):
        objDics.append( handleObjectTag(obj) )
    return objDics

def handleObjectTag(objectElement):
    dic = {}
    dic["name"] = objectElement.getElementsByTagName("name")[0].childNodes[0].data
    dic["id"] = objectElement.getElementsByTagName("id")[0].childNodes[0].data
    dic["type"] = objectElement.getElementsByTagName("type")[0].childNodes[0].data
    dic["clr"] = objectElement.getElementsByTagName("clr")[0].childNodes[0].data
    dic["points"] = getPoints(objectElement)
    return dic

def getPoints(objectElement):
    points = []
    for (x,y) in zip(objectElement.getElementsByTagName("points")[0].getElementsByTagName("x"), 
        objectElement.getElementsByTagName("points")[0].getElementsByTagName("y")):
        points.append((float(x.childNodes[0].data), float(y.childNodes[0].data)))
    
    return points

