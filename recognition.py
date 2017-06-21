import cv2
import numpy as np
from os.path import join, isfile
from os import listdir
from time import time

'''
Main function

This function gets the image of planes from space
and recognize planes on it. Requires Haar cascade.

Recognizing parameters given as ranges to iterate values.

Write an image to folder if needed.
Shows the image with rectangles in window.
'''


def detectObjects(img,
                  casc,
                  neighborsRange,
                  scaleRange,
                  sizeRange,
                  writeResults=False):

    checks_count = 0
    all_rects = []
    img_to_rec = np.copy(img)

    for minNeighbors in range(neighborsRange[0],
                              neighborsRange[1]):
        for scale in [float(i / 10.0) for i in range(scaleRange[0],
                                                     scaleRange[1])]:
            for minSize in range(sizeRange[0],
                                 sizeRange[1],
                                 sizeRange[2]):

                objects = casc.detectMultiScale(
                    img_to_rec,
                    scale,
                    minNeighbors,
                    minSize=(minSize, minSize)
                )

                inside_rectangles_indexes = []
                for i in range(len(objects)):
                    if isRectInsideAnother(objects[i], objects):
                        inside_rectangles_indexes.append(i)
                objects = np.delete(objects,
                                    inside_rectangles_indexes,
                                    0)

                img_to_rec = np.copy(img)

                all_rects.extend(objects)
                checks_count += 1

    avg_rects = getAvgRects(all_rects)
    clear_rects = list(avg_rects)

    for rect in avg_rects:
        x, y, w, h, c = rect
        rang = float(c * 100 / checks_count)
        if rang < 70:
            clear_rects.remove(rect)

    img_res = np.copy(img)

    drawObjectRects(img_res, clear_rects)
    displayImage(img_res, "Result")

    if writeResults:
        cv2.imwrite(join(results_path,
                         "result_%.5f.png" % (time())), img_res)

    getKey()


'''
Get center of the rectangle

This function transforms the classic CV
rectangle representation to another.

Return the tuple of tuples, where 1st tuple is
x and y of rectangle and 2nd tuple is width and height
'''


def getRectangleCenter(rect):
    return ((rect[0] + rect[2] / 2,
             rect[1] + rect[3] / 2),
            (rect[2], rect[3]))


def checkInnerRects(src, rects, casc, scale=1.5):
    if rects is None or len(rects) == 0:
        return rects

    res_rects = np.copy(rects)
    remove_indexes = []
    for i in range(len(rects)):
        rec = rects[i]
        rec_image = getImageInRectangle(src, rec, ran=10)
        inner_recs = casc.detectMultiScale(
            rec_image,
            scale,
            2,
            minSize=(int(rec[2] / 1.5),
                     int(rec[3] / 1.5))
        )
        if len(inner_recs) == 0:
            remove_indexes.append(i)
    print remove_indexes
    res_rects = np.delete(res_rects, remove_indexes, axis=0)
    return res_rects


def getAvgRects(rectangles, threshold=25):

    grouped = []
    rects = [getRectangleCenter(r) for r in rectangles]

    while(len(rects) > 0):
        tmp_group = []
        tmp_group.append(rects[0])
        for rect in rects[1:]:
            avg_x = float(
                sum([r[0][0] for r in tmp_group]) / len(tmp_group)
            )
            avg_y = float(
                sum([r[0][1] for r in tmp_group]) / len(tmp_group)
            )

            cur_x = rect[0][0]
            cur_y = rect[0][1]

            if (cur_x < avg_x + threshold and
                cur_x > avg_x - threshold and
                cur_y < avg_y + threshold and
                cur_y > avg_y - threshold):

                tmp_group.append(rect)

        gr_avg_w = sum([r[1][0] for r in tmp_group]) / len(tmp_group)
        gr_avg_h = sum([r[1][1] for r in tmp_group]) / len(tmp_group)
        gr_avg_x = sum([r[0][0] for r in tmp_group]) / len(tmp_group)
        gr_avg_y = sum([r[0][1] for r in tmp_group]) / len(tmp_group)

        grouped.append((gr_avg_x - gr_avg_w / 2,
                        gr_avg_y - gr_avg_h / 2,
                        gr_avg_w, gr_avg_h,
                        len(tmp_group)))

        for t_r in tmp_group:
            rects.remove(t_r)
        tmp_group = []
    return grouped


'''
Get key method

Function which requests a key from user pressed in
CV2 windows. Waiting time sets as optional argument
measured in miliseconds.

time = 0 means that function will wait until any key
is not pressed.

Returns a code of the pressed key.
'''


def getKey(time=0):
    keycode = cv2.waitKey(time)
    if keycode != -1:
        return keycode & 0xFF


'''
Draw rectangles method

Function which draws the rectangles given in
argument rects to the image in argument img.

Color sets as an optional argument.
'''


def drawObjectRects(img, rects, color=(20, 20, 250)):
    if rects is None:
        return
    for rect in rects:
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), color)


'''
Function which checks if one rectangle is fully
in the any of another rectangles. Uses a coordiants to
compare. Returns True or False
'''


def isRectInsideAnother(rect_to_check, all_rects):
    xc, yc, wc, hc = rect_to_check

    for another_rect in all_rects:
        xa, ya, wa, ha = another_rect

        if (xc > xa and
            yc > ya and
            yc + hc < ya + ha and
            xc + wc < xa + wa):

            return True
    return False


'''
Simple wrapper function to display images
in the CV2 window.
'''


def displayImage(img, winname):
    cv2.imshow(winname, img)


'''
Function which returns a part of image which
is inside the rectangle. Image takes from the
"rect" argument, rectangle from "rect" arg.

ran argument uses to increase rect region with
given number of pixels. If your rect is 200 px width
and ran = 10 then you will get an image 220 px width

'''

def getImageInRectangle(source, rect, ran=0):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]

    try:
        return np.copy(source[y - ran:y + h + ran,
                              x - ran:x + w + ran])
    except Exception:
        if ran != 0:
            return getImageInRectangle(source, rect, ran=ran - 1)
        else:
            return getImageInRectangle(source, rect, ran=0)


'''
Constants definiton
'''
results_path = "./results/"
test_path = "./test_images/"
cascades_path = "/home/artemka/PlanesRecognition/cascade_training/"

'''
Get a list of pathes to test images
'''
test_images = [join(test_path, filename) for
               filename in listdir(test_path) if
               isfile(join(test_path, filename))]

'''
Create a list of cascade objects
'''
cascades = {
    "no_filter": cv2.CascadeClassifier(
        join(cascades_path,
             "cascade_orig/cascade.xml")),
    "gray": cv2.CascadeClassifier(
        join(cascades_path,
             "cascade_gray/cascade.xml")),
    "blur": cv2.CascadeClassifier(
        join(cascades_path,
             "cascade_blur/cascade.xml")),
    "canny": cv2.CascadeClassifier(
        join(cascades_path,
             "cascade_canny/cascade.xml")),
    "gray_blur": cv2.CascadeClassifier(
        join(cascades_path,
             "cascade_gray_blur/cascade.xml"))
}



'''
Iterate all of test images
'''
for img in [cv2.imread(test_im) for test_im in test_images]:

    detectObjects(
        img,
        cascades["no_filter"],
        (3, 6),
        (11, 22),
        (15, 25, 5),
        writeResults=True
    )

cv2.waitKey(0)
