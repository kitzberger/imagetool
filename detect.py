#!/bin/env python3

import cv2
import sys
import numpy as np
import os

def cut(in_path, out_path, thresh1 = 155, thresh2 = 100):
    """
    Isolate objects in front of a white-ish background by making that background transparent
    TODO:  * autodetect thresholds
           * throw hull around detected objects to prevent enclaves being made transparent
    """
    path = in_path
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    mask = img

    # make binary mask so findCountours can do its thing
    ret, mask = cv2.threshold(mask, thresh1, 204, cv2.THRESH_TRUNC)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = cv2.blur(mask, (20, 20))
    mask = cv2.bitwise_not(mask, mask)

    kernel = np.ones((5,5),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations = 1)
    ret, mask = cv2.threshold(mask, thresh2, 255, cv2.THRESH_BINARY)

    # mask out unwanted parts
    img = cv2.bitwise_and(img, img, mask=mask)

    # and make transparent
    alpha = mask
    b, g, r = cv2.split(img)
    rgba = [b, g, r, alpha]
    img = cv2.merge(rgba, 4)

    cv2.imwrite(out_path, img)

def main():
    thresh1 = 155
    thresh2 = 100

    if len(sys.argv) > 1:
        thresh1 = int(sys.argv[1])
    if len(sys.argv) > 2:
        thresh2 = int(sys.argv[2])

    print('Using thresholds: ' + str(thresh1) + ' and ' + str(thresh2))

    out_dir = "./out"

    os.makedirs(out_dir, exist_ok=True)

    extensions = (".jpeg", ".JPEG", ".jpg", ".JPG")

    counter = 0

    for ext in extensions:
        for img_path in os.listdir(os.getcwd()):
            if img_path.endswith(ext):
                try:
                    img_path_out = out_dir + "/" + os.path.splitext(os.path.basename(img_path))[0] + ".png"
                    cut(img_path, img_path_out, thresh1, thresh2)
                    sys.stdout.write(".")
                    counter += 1
                except Exception as e:
                    sys.stdout.write("x")
                sys.stdout.flush()

    print('')
    print('Processed a total of ' + str(counter) + ' image files.')

if __name__ == "__main__":
    main()

