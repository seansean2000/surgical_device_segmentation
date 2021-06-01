import xml.dom.minidom
import os
import glob
import numpy as np
import cv2

surgical_tools = ["Obturator", "Robotic Bipolar Forceps", "Robotic Graspers", "Suction Irrigator", "Clip Applier", "Assistant Port",
                 "Trocar", "Graspers", "Fixation Forceps", "Tenaculum", "Dissectors", "Harmonic Scapel", "Hook Suction", 
                  "Spatula Suction", "Clip", "Retrieval Bag", "Irrigator", "Straighted Needle", "Needle Holder", "Endo GI Stapler", 
                 "Stapler", "Gauze", "Cotton Bundle", "Liver Retractor", "Cautery Hook"]
# 25 tools in total


def handleXmlAnnotation(xmlAnnotationPath):

    annotateDic = {'objects':[]}
    
    with xml.dom.minidom.parse(xmlAnnotationPath) as doc:
        for obj in doc.getElementsByTagName("object"):
            annotateDic["objects"].append(handleObjectTag(obj))
        
        annotateDic["folder"] = doc.getElementsByTagName("folder")[0].childNodes[0].data
        annotateDic["filename"] = doc.getElementsByTagName("filename")[0].childNodes[0].data
        annotateDic["path"] = doc.getElementsByTagName("path")[0].childNodes[0].data
        
    return annotateDic


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


def handleFolder(folderPath, XMLarray):
    for fileName in glob.glob(os.path.join(folderPath,'*.xml')):
        XMLarray.append(handleXmlAnnotation(fileName))
        
        
        
def fillOutLine (singleXML, originalimg, saveLocation, imgName):
    for obj in singleXML["objects"]:
        ptsArray = []
        for points in obj["points"]:
            ptsArray.append([int(points[0]), int(points[1])]) #points[0] = x coordinate, points[1] = y coordinate
            
        
        try:
            mask_color = surgical_tools.index(obj["name"]) + 231 #"Obturator" will have color (231,231,231) and Cautery Hook will be 255
        except Exception as e:
            mask_color = 100
            print(e)
        
        ptsNumpy = np.array(ptsArray)
        ptsNumpy = ptsNumpy.reshape((-1,1,2))
        cv2.fillPoly(originalimg, [ptsNumpy], [mask_color, mask_color, mask_color])
        
    cv2.imwrite(os.path.join(saveLocation, imgName), originalimg)

    
def segmentImageinFolder(saveLocation, XMLarray):
    for singleXMLFile in XMLarray:
        imgName = singleXMLFile["filename"]
        img = np.zeros((1080, 1920, 3), np.uint8) # Creates a new black image of 1920 X 1080 and draws the tools on top of it
        fillOutLine(singleXMLFile, img, saveLocation, imgName)
        
saveLocation = './Masked Images' #the location to save the mask images
folderPath = "./data" #this location should store all the xml files and the corresponding images
allXMLinFolder = [] #this is the array that will store all the XML files in the 'data' folder

handleFolder(folderPath, allXMLinFolder)
segmentImageinFolder(saveLocation, allXMLinFolder)

#print(allXMLinFolder[0]["objects"][0]["name"])