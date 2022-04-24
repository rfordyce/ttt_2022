#!/usr/bin/env python3

import base64
import os
import time
from contextlib import contextmanager

import cv2  # for board reading - should this be trained or ugly dynamic?
import numpy as np
from redis import Redis  # for distributed queue

# should this use a display queue and thread?
#   practically to prefer over gross python logging
#   otherwise feed into redis queue --> display on API/UI via socket?..

RED   = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE  = (255, 0, 0)


@contextmanager
def capture_device(webcam_device="/dev/video0"):
    cap = cv2.VideoCapture(webcam_device)
    try:
        yield cap
    finally:
        cap.release()


def build_template_matchers():

    class TemplateMatcher():

        def __init__(self, path_img, threshold=0.8, color=RED):
            # TODO allow passing img
            self.template  = cv2.imread(path_img, cv2.IMREAD_GRAYSCALE)
            self.threshold = threshold
            self.color     = color

        def matches(self, img):  # TODO does it make sense for this to be __call__(...)?
            try:
                img_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
            except Exception as ex:  # FIXME hack to accept already greyscale images
                if "Invalid number of channels in input image" not in str(ex):
                    raise ex
                img_gray = img.copy()
            res = cv2.matchTemplate(img_gray, self.template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)
            return zip(*loc[::-1]), res * 255.0  # fix TM_CCOEFF_NORMED, 0-1 to greyscale

        def draw(self, img):
            img = img.copy()
            w, h = self.template.shape[::-1]  # TODO just make these properties?
            cutoffs, img_prb = self.matches(img)
            for pt in cutoffs:
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), self.color, 2)
            return img, img_prb

    # load and clean up images for templates
    return {  # threshold badly tuned for TM_CCOEFF_NORMED
        "grid": TemplateMatcher("templates/grid_01.bmp", 0.6, BLUE),
        "O":    TemplateMatcher("templates/O_01.bmp", 0.2, GREEN),  # XXX horrible need DTM instead
        "X":    TemplateMatcher("templates/X_01.bmp", 0.2, RED),
    }


def board_cleanup(img):
    # orig = img  # keep a reference
    img    = img.copy()
    img    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img    = cv2.GaussianBlur(img, (5, 5), 0)
    # thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    img = cv2.Canny(img, 100, 200)  # sharp cutoff cleanup
    img = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=5)
    # return img, img  # FIXME return cleaned, annotated (histogram?)
    im1 = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2RGB)  # XXX
    return im1, img  # FIXME return cleaned, annotated (histogram?)


def read_board(webcam):
    ret, frame = webcam.read()  # read one frame

    # clean up the image
    cleaned, annotated = board_cleanup(frame)

    # convert to board
    board = []
    return frame, cleaned, annotated, board
    # return img_frame, img_cnt, board
    # return img_frame, img_cleaned, board


def surrender_loop():
    while True:
        if "check if board is cleared":
            break
        # should this explicitly drive arm to fixed positions?
        "clear surrender action series"


def img_raw_b64(img):
    # https://stackoverflow.com/a/40930153/
    return base64.b64encode(cv2.imencode('.png', img)[1])


def contourifier(img):
    # take a look at
    #   https://stackoverflow.com/a/52865864/
    #   https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
    #   https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # extract contours
    # ret, thresh = cv2.threshold(img_grey, 127, 255, 0)
    thresh = cv2.adaptiveThreshold(img_grey, 127, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 20)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_cnt = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    # img_cnt = cv2.imencode(".jpg", img_cnt)

    return img_cnt


def main():
    # offer to discover webcam device?
    redis_handle = Redis(os.environ["ADDRESS_CACHE"])
    matchers = build_template_matchers()

    with capture_device() as webcam:
        while True:
            # read Q (redis)? (may have explicit moves?)
            frame, cleaned, annotated, board = read_board(webcam)
            redis_handle.set("webcam_view", img_raw_b64(frame))

            img_cnt, img_prb = matchers["X"].draw(cleaned)
            img_cnt, img_prb = matchers["O"].draw(img_cnt)
            img_cnt, _ = matchers["grid"].draw(img_cnt)
            redis_handle.set("img_cnt", img_raw_b64(img_cnt))
            redis_handle.set("img_prb", img_raw_b64(img_prb))
            # redis_handle.set("img_prb", img_raw_b64(thresh))

            if not "check if it's my turn":
                time.sleep(1)  # TODO async?
                continue  # next iteration
            "check if game is lost"  # --> surrender action loop
            "calculate next move"
            "make next move"
            "verify move was made correctly"  # stretch goal? --> may help debug high-level
            # feed back to Q at end of loop?


if __name__ == "__main__":
    # argparser
    # discover camera device?
    # import os
    # webcam_device = os.environ["WEBCAM_DEVICE"]
    # main(webcam_device)

    # FIXME is it acceptable to let opencv detect camera each time? maybe slow
    #   still, it's probably better to continuously capture frames and detect in them
    #   perhaps snagging motion and combining them for something
    #   suspect this will lead to much better detection
    main()
