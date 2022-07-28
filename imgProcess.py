import cv2
import cv2 as cv
from transform import four_point_transform

def TransContour(image,contours,number):
    ans_block = []
    for i in range(number):
        cv.drawContours(image, contours[i], -1, (0, 255, 0), 0)
        wrapped = four_point_transform(image,contours[i])
        ans_block.append(wrapped)
    return ans_block
def AnsBoxProcess(ans_block):
    ans_box = []
    for block in ans_block:
        for i in range(6):
            (h, w) = block.shape
            temp_h = h//6
            ans_box.append(block[temp_h*i:temp_h*(i+1),0:w])

    return ans_box
def AnsCellProcess(ans_box):
    ans_cell = []
    for box in ans_box:
        (h,w) = box.shape
        h_ratio = h // 12
        w_ratio = w // 4
        temp_img = box[0 + h_ratio:h - h_ratio, 0 + w_ratio:w-w//12]
        for i in range(5):
            h, w = temp_img.shape
            temp_h = h // 5
            ans_cell.append(temp_img[temp_h * i:temp_h * (i + 1), 0:w])

    return ans_cell
def AnsListProcess(ans_cell):
    ans_list = []
    for cell in ans_cell:
        for i in range(4):
            h, w = cell.shape
            temp_w = w // 4
            ans_list.append(cell[0:h, temp_w*i:temp_w*(i+1)])
    return ans_list
def ExportJSON(ans_list):
    AnsDict = {}
    counter = 1
    tempAns = ""
    checker = 0
    for idx,item in enumerate(ans_list):
        temp_imgGray = cv.GaussianBlur(item,(9,9),7)
        ret, threshold2 = cv.threshold(temp_imgGray,190,300,cv.THRESH_BINARY)
        value = cv.countNonZero(threshold2)
        if value < 650:
            if (idx+1)%4 == 1:
                tempAns= "A"
                checker += 1
            if (idx+1)%4 == 2:
                tempAns= "B"
                checker += 1
            if (idx+1)%4 == 3:
                tempAns= "C"
                checker += 1
            if (idx+1)%4 == 0:
                tempAns= "D"
                checker += 1
        if (idx+1)%4==0:
            if checker >1:
                tempAns=""
            AnsDict[counter] = tempAns
            tempAns=""
            counter += 1
            checker = 0
    return AnsDict
def IDListProcess(id_block,col_num):
    id_list = []
    for i in range(col_num):
        h,w = id_block.shape
        temp_w= w // col_num
        for y in range(10):
            temp_h = h//10
            id_list.append(id_block[temp_h * y: temp_h * (y + 1),temp_w*i:temp_w*(i+1)])

    return id_list
def IDJson(id_list):
    Id = ""
    checker=0
    for idx, item in enumerate(id_list):

        temp_imgGray = cv.GaussianBlur(item, (9, 9), 7)
        ret, threshold2 = cv.threshold(temp_imgGray, 190, 300, cv.THRESH_BINARY)
        value = cv.countNonZero(threshold2)
        if value < 650:
            for i in range(9,0,-1):
                if (idx+1)%10==i:
                    Id = Id + str(i-1)
                    checker += 1
        if (idx + 1) % 10 == 0:
            if value <650:
                Id = Id + str(9)
                checker+=1
            if checker > 1:
                Id[len(Id)-1] = "X"
                break
            checker = 0
    return Id

