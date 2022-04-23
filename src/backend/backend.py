#!/usr/bin/env python3

import os
import time
from contextlib import contextmanager

import cv2  # for board reading - should this be trained or ugly dynamic?
# import numpy as np
from redis import Redis  # for distributed queue

# should this use a display queue and thread?
#   practically to prefer over gross python logging
#   otherwise feed into redis queue --> display on API/UI via socket?..


@contextmanager
def capture_device(webcam_device="/dev/video0"):
    cap = cv2.VideoCapture(webcam_device)
    try:
        yield cap
    finally:
        cap.release()


def read_board(webcam):
    ret, frame = webcam.read()  # read one frame
    # convert to board
    board = []
    return frame, board


def surrender_loop():
    while True:
        if "check if board is cleared":
            break
        # should this explicitly drive arm to fixed positions?
        "clear surrender action series"


def img_raw_b64(img):
    assert img.shape == (480, 640, 3)  # XXX probably no reason to bother with this

    # https://stackoverflow.com/a/40930153/
    import base64
    retval, buffer = cv2.imencode('.png', img)
    return base64.b64encode(buffer)


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

    with capture_device() as webcam:
        while True:
            # read Q (redis)? (may have explicit moves?)
            frame, board = read_board(webcam)
            redis_handle.set("webcam_view", img_raw_b64(frame))

            img_cnt = contourifier(frame)  # XXX
            redis_handle.set("img_cnt", img_raw_b64(img_cnt))

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
