#!/usr/bin/env python3

import os
import time

import cv2  # for board reading - should this be trained or ugly dynamic?
# import numpy as np
from redis import Redis  # for distributed queue

# should this use a display queue and thread?
#   practically to prefer over gross python logging
#   otherwise feed into redis queue --> display on API/UI via socket?..


def read_board(webcam_device):
    # https://stackoverflow.com/a/56354464/
    # TODO rewrite as a context manager if using open:read:close strategy
    cap = cv2.VideoCapture(webcam_device)  # pass device?
    ret, frame = cap.read()  # read one frame
    cap.release()  # release the VideoCapture object
    # some detection if the frame is trash (can this happen?)
    # what if the webcam is slow?
    # what if the webcam is out of focus (mine probably has autofocus)
    #   honestly, less focus may be better for this ugly detection anyways

    print(frame.shape)  # how to pretty print
    print(frame)  # how to pretty print
    # print(np.matrix(frame))
    return frame


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


def main(webcam_device):
    # offer to discover webcam device?
    redis_handle = Redis(os.environ["ADDRESS_CACHE"])

    while True:
        # read Q (redis)? (may have explicit moves?)
        state_board = read_board(webcam_device)  # FIXME do we need to pass device?
        # redis_handle(state_board)  # XXX just for display on UI
        redis_handle.set("webcam_view", img_raw_b64(state_board))
        # redis_handle.set("webcam_view", "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")  # XXX just for display on UI
        if not "check if it's my turn":
            time.sleep(1)  # TODO async?
            continue  # next iteration
        time.sleep(600)  # XXX make a long loop - camera clicks uncomfortably
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
    main("/dev/video0")
