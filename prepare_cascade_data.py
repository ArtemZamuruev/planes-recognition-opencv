import os
import cv2
from os.path import join, isfile


good_path = "./planes_good/"
bad_path = "./planes_bad/"

orig_path = "orig/"
gray_path = "gray/"
blur_path = "blur/"
canny_path = "canny/"
gray_and_blur_path = "gray_and_blur/"
gray_and_canny_path = "gray_and_canny/"
gray_and_blur_and_canny_path = "gray_and_blur_and_canny/"

data_good = "good"
data_bad = "bad"

data_orig = "orig"
data_gray = "gray"
data_blur = "blur"
data_canny = "canny"
data_gray_and_blur = "gray_and_blur"
data_gray_and_canny = "gray_and_canny"
data_gray_and_blur_and_canny = "gray_and_blur_and_canny"


# 1 - counter
# 2 - bad or good
# 3 - type
img_name_pattern = "%.3d_%s_%s.png"


# 1 - filename with path
# 2 - width
# 3 - height
dataline_pattern_good = "%s 1 0 0 %d %d\n"
dataline_pattern_bad = "%s\n"

# 1 - bad or good
# 2 - type
datafile_patern = "%s_%s.dat"


blur_kernel_size = 7
blur_gamma = 2.5

canny_t1 = 60
canny_t2 = 100


src_files_good = [join(good_path, orig_path, f) for f in os.listdir(join(good_path, orig_path)) if isfile(join(good_path, orig_path, f))]
src_files_bad = [join(bad_path, orig_path, f) for f in os.listdir(join(bad_path, orig_path)) if isfile(join(bad_path, orig_path, f))]

def handle_good_images():
    counter = 0

    datafile_orig = open(datafile_patern % (data_good, data_orig), "a")
    datafile_gray = open(datafile_patern % (data_good, data_gray), "a")
    datafile_blur = open(datafile_patern % (data_good, data_blur), "a")
    datafile_canny = open(datafile_patern % (data_good, data_canny), "a")
    datafile_gray_and_blur = open(datafile_patern % (data_good, data_gray_and_blur), "a")
    datafile_gray_and_canny = open(datafile_patern % (data_good, data_gray_and_canny), "a")
    datafile_gray_and_blur_and_canny = open(datafile_patern % (data_good, data_gray_and_blur_and_canny), "a")

    for file in src_files_good:

        counter += 1

        # Reading image
        img_orig = cv2.imread(file)

        width, height, nchannels = img_orig.shape

        # Saving to the new name and writing to data file
        newname_orig = join(good_path, orig_path, img_name_pattern % (counter, data_good, data_orig))
        cv2.imwrite(newname_orig, img_orig)
        datafile_orig.write(dataline_pattern_good % (newname_orig, width, height))

        # Graying image
        img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
        newname_gray = join(good_path, gray_path, img_name_pattern % (counter, data_good, data_gray))
        cv2.imwrite(newname_gray, img_gray)
        datafile_gray.write(dataline_pattern_good % (newname_gray, width, height))

        # Bluring image
        img_blur = cv2.GaussianBlur(img_orig, (blur_kernel_size, blur_kernel_size), blur_gamma)
        newname_blur = join(good_path, blur_path, img_name_pattern % (counter, data_good, data_blur))
        cv2.imwrite(newname_blur, img_blur)
        datafile_blur.write(dataline_pattern_good % (newname_blur, width, height))

        # Canny image
        img_canny = cv2.Canny(img_orig, canny_t1, canny_t2)
        newname_canny = join(good_path, canny_path, img_name_pattern % (counter, data_good, data_canny))
        cv2.imwrite(newname_canny, img_canny)
        datafile_canny.write(dataline_pattern_good % (newname_canny, width, height))

        # Gray and blur
        img_gray_and_blur = cv2.GaussianBlur(img_gray, (blur_kernel_size, blur_kernel_size), blur_gamma)
        newname_gray_and_blur = join(good_path, gray_and_blur_path, img_name_pattern % (counter, data_good, data_gray_and_blur))
        cv2.imwrite(newname_gray_and_blur, img_gray_and_blur)
        datafile_gray_and_blur.write(dataline_pattern_good % (newname_gray_and_blur, width, height))

        # Gray and canny
        img_gray_and_canny = cv2.Canny(img_gray, canny_t1, canny_t2)
        newname_gray_and_canny = join(good_path, gray_and_canny_path, img_name_pattern % (counter, data_good, data_gray_and_canny))
        cv2.imwrite(newname_gray_and_canny, img_gray_and_canny)
        datafile_gray_and_canny.write(dataline_pattern_good % (newname_gray_and_canny, width, height))

        # Gray and blur and Canny 
        img_all = cv2.Canny(img_gray_and_blur, canny_t1, canny_t2)
        newname_all = join(good_path, gray_and_blur_and_canny_path, img_name_pattern % (counter, data_good, data_gray_and_blur_and_canny))
        cv2.imwrite(newname_all, img_all)
        datafile_gray_and_blur_and_canny.write(dataline_pattern_good % (newname_all, width, height))

        print "File %d is ready ..." % (counter)

    datafile_orig.close()
    datafile_gray.close()
    datafile_blur.close()
    datafile_canny.close()
    datafile_gray_and_blur.close()
    datafile_gray_and_canny.close()
    datafile_gray_and_blur_and_canny.close()





def handle_bad_images():
    counter = 0

    datafile_orig = open(datafile_patern % (data_bad, data_orig), "a")
    datafile_gray = open(datafile_patern % (data_bad, data_gray), "a")
    datafile_blur = open(datafile_patern % (data_bad, data_blur), "a")
    datafile_canny = open(datafile_patern % (data_bad, data_canny), "a")
    datafile_gray_and_blur = open(datafile_patern % (data_bad, data_gray_and_blur), "a")
    datafile_gray_and_canny = open(datafile_patern % (data_bad, data_gray_and_canny), "a")
    datafile_gray_and_blur_and_canny = open(datafile_patern % (data_bad, data_gray_and_blur_and_canny), "a")

    for file in src_files_bad:

        counter += 1

        # Reading image
        img_orig = cv2.imread(file)

        width, height, nchannels = img_orig.shape

        # Saving to the new name and writing to data file
        newname_orig = join(bad_path, orig_path, img_name_pattern % (counter, data_bad, data_orig))
        cv2.imwrite(newname_orig, img_orig)
        datafile_orig.write(dataline_pattern_bad % (newname_orig))

        # Graying image
        img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
        newname_gray = join(bad_path, gray_path, img_name_pattern % (counter, data_bad, data_gray))
        cv2.imwrite(newname_gray, img_gray)
        datafile_gray.write(dataline_pattern_bad % (newname_gray))

        # Bluring image
        img_blur = cv2.GaussianBlur(img_orig, (blur_kernel_size, blur_kernel_size), blur_gamma)
        newname_blur = join(bad_path, blur_path, img_name_pattern % (counter, data_bad, data_blur))
        cv2.imwrite(newname_blur, img_blur)
        datafile_blur.write(dataline_pattern_bad % (newname_blur))

        # Canny image
        img_canny = cv2.Canny(img_orig, canny_t1, canny_t2)
        newname_canny = join(bad_path, canny_path, img_name_pattern % (counter, data_bad, data_canny))
        cv2.imwrite(newname_canny, img_canny)
        datafile_canny.write(dataline_pattern_bad % (newname_canny))

        # Gray and blur
        img_gray_and_blur = cv2.GaussianBlur(img_gray, (blur_kernel_size, blur_kernel_size), blur_gamma)
        newname_gray_and_blur = join(bad_path, gray_and_blur_path, img_name_pattern % (counter, data_bad, data_gray_and_blur))
        cv2.imwrite(newname_gray_and_blur, img_gray_and_blur)
        datafile_gray_and_blur.write(dataline_pattern_bad % (newname_gray_and_blur))

        # Gray and canny
        img_gray_and_canny = cv2.Canny(img_gray, canny_t1, canny_t2)
        newname_gray_and_canny = join(bad_path, gray_and_canny_path, img_name_pattern % (counter, data_bad, data_gray_and_canny))
        cv2.imwrite(newname_gray_and_canny, img_gray_and_canny)
        datafile_gray_and_canny.write(dataline_pattern_bad % (newname_gray_and_canny))

        # Gray and blur and Canny
        img_all = cv2.Canny(img_gray_and_blur, canny_t1, canny_t2)
        newname_all = join(bad_path, gray_and_blur_and_canny_path, img_name_pattern % (counter, data_bad, data_gray_and_blur_and_canny))
        cv2.imwrite(newname_all, img_all)
        datafile_gray_and_blur_and_canny.write(dataline_pattern_bad % (newname_all))

        print "File %d is ready ..." % (counter)

    datafile_orig.close()
    datafile_gray.close()
    datafile_blur.close()
    datafile_canny.close()
    datafile_gray_and_blur.close()
    datafile_gray_and_canny.close()
    datafile_gray_and_blur_and_canny.close()

# handle_good_images()


handle_bad_images()
