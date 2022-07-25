import cv2
import cv2 as cv
from transform import detectPts
import imgProcess as pros
from flask import jsonify

def GetPoint(img):
    image_read = cv2.imread("test.jpg")
    if image_read.shape[0]< image_read.shape[1]:
        image_read = cv2.rotate(image_read,cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_resize = cv2.resize(image_read, (1102, 1560))
    image = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    img_cropped = image[image.shape[0] // 4:image.shape[0], 0:image.shape[1]]
    threshold = cv2.threshold(img_cropped, 200, 255, cv2.THRESH_BINARY)[1]
    img2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cts = contours[1:5]
    cv2.drawContours(img_cropped, cts, -1, (0, 0, 255), 5)
    for i in range(4):
        for y in range(i, 4):
            rect = detectPts(cts[i])
            (topL, topR, botR, botL) = rect
            rect2 = detectPts(cts[y])
            (topL2, topR2, botR2, botL2) = rect2
            if topL[0] > topL2[0]:
                tempCt = cts[i]
                cts[i] = cts[y]
                cts[y] = tempCt

    ansBlock = pros.TransContour(img_cropped,cts,4)
    ansBox = pros.AnsBoxProcess(ansBlock)
    ansCell = pros.AnsCellProcess(ansBox)
    ansList = pros.AnsListProcess(ansCell)
    ansJSON = pros.ExportJSON(ansList)
    return ansJSON
def GetID(img):
    image_read = cv2.imread("test.jpg")
    if image_read.shape[0] < image_read.shape[1]:
        image_read = cv2.rotate(image_read, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_resize = cv2.resize(image_read, (1102, 1560))
    image = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    img_croptop = image[0:image.shape[0] // 3, 0:image.shape[1]]
    threshold = cv2.threshold(img_croptop, 200, 255, cv2.THRESH_BINARY)[1]
    img2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cts = contours[3],contours[5]
    # cv2.drawContours(img_croptop, cts, -1, (0, 0, 255), 5)

    IDBlock = pros.TransContour(img_croptop,cts,2)

    IDList = pros.IDListProcess(IDBlock[0],6)
    TestIDList = pros.IDListProcess(IDBlock[1],3)

    StudentID = pros.IDJson(IDList)
    TestID = pros.IDJson(TestIDList)
    result={}
    result["StudentID"]=StudentID
    result["TestID"]=TestID
    return result
