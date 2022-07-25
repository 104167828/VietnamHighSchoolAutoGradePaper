
import numpy as np
import cv2 as cv
def detectPts(ct):
    rect = np.zeros((4, 2), dtype="float32")
    peri = cv.arcLength(ct, True)
    corners = cv.approxPolyDP(ct, 0.04 * peri, True)
    topL = corners[0][0]
    # top-left
    topR = corners[1][0]
    # top-right
    botR = corners[2][0]
    # bottom-right
    botL = corners[3][0]
    # bottom-left
    pts = np.array([(topL[0],topL[1]),(topR[0],topR[1]),(botR[0],botR[1]),(botL[0],botL[1])])
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect
def four_point_transform(image,ct):

    rect = detectPts(ct)
    (topL, topR, botR, botL) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    src_pts = np.array([topL, topR, botR, botL], dtype=np.float32)

    widthA = np.sqrt(((botR[0] - botL[0]) ** 2) + ((botR[1] - botL[1]) ** 2))
    widthB = np.sqrt(((topR[0] - topL[0]) ** 2) + ((topR[1] - topL[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((topR[0] - botR[0]) ** 2) + ((topR[1] - botR[1]) ** 2))
    heightB = np.sqrt(((topL[0] - botL[0]) ** 2) + ((topL[1] - botL[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
    # construct the argument parse and parse the arguments
    M = cv.getPerspectiveTransform(src_pts, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped
