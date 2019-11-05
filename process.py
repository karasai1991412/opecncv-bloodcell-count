# import libraries here
import cv2
import numpy as np
param_kernel_morph = (10,10)
param_kernel_deliate = (12,12)
param_min_area = 2000
param_max_area = 12000
# ((4, 4), (8, 8), 2000, 12000) 80.55555555555556
# ((8, 8), (10, 10), 2000, 12000) 83.33333333333333
# ((8, 8), (10, 10), 2000, 13000) 91.66666666666667
# ((10, 10), (12, 12), 2000, 12000) 100.0
def colorfilterbyred(img,morph = param_kernel_morph,deliate = param_kernel_deliate,min_area = param_min_area,max_area= param_max_area):
    #convert image to hsv to apply red color filter
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,15,5])
    upper_red = np.array([20,50,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([150,15,5])
    upper_red = np.array([180,50,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    # join my masks
    mask = mask0+mask1

    # extract cell area using morph transform
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,morph) # default:(10,10)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    kernel = np.ones(deliate,np.uint8)
    dilation = cv2.dilate(opening,kernel,iterations = 1)
    _,cnts,_ = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    bonus = 0
    for c in cnts:
        #check if a cell is valid by area
        if(cv2.contourArea(c)>min_area):
            # if area  is more than max_value, then assum that the area contain more than one cell
            if(cv2.contourArea(c)>max_area):
                bonus += int(cv2.contourArea(c)/max_area)
                pass
            rect = cv2.boundingRect(c)
            rects.append(rect)
            pass
        else:
            pass
        pass
    return img,len(rects)+bonus
    pass
def count_blood_cells(image_path):
    """
    Procedura prima putanju do fotografije i vraca broj krvnih zrnaca.

    Ova procedura se poziva automatski iz main procedure i taj deo kod nije potrebno menjati niti implementirati.

    :param image_path: <String> Putanja do ulazne fotografije.
    :return: <int>  Broj prebrojanih krvnih zrnaca
    """
    blood_cell_count = 0
    # TODO - Prebrojati krvna zrnca i vratiti njihov broj kao povratnu vrednost ove procedure
    img = cv2.imread(image_path)
    # get total count of red cells
    img,count_red_cell = colorfilterbyred(img.copy())
    return count_red_cell