import time

import cv2  # for board reading - should this be trained or ugly dynamic?
# import redis  # for distributed queue

# should this use a display queue and thread?
#   practically to prefer over gross python logging
#   otherwise feed into redis queue --> display on API/UI via socket?..


def read_board(webcam_device):
    # https://stackoverflow.com/a/56354464/
    # TODO rewrite as a context manager if using open:read:close strategy
    cap = cv2.VideoCapture(webcam_device)  # pass device?
    if not cap.isOpened():  # from opencv docs
        print("Cannot open camera")
    ret, frame = cap.read()  # read one frame
    print(frame.shape)
    cap.release()  # release the VideoCapture object
    # some detection if the frame is trash (can this happen?)
    # what if the webcam is slow?
    # what if the webcam is out of focus (mine probably has autofocus)
    #   honestly, less focus may be better for this ugly detection anyways


def surrender_loop():
    while True:
        if "check if board is cleared":
            break
        # should this explicitly drive arm to fixed positions?
        "clear surrender action series"


def main(webcam_device):
    # offer to discover webcam device?
    while True:
        # read Q (redis)? (may have explicit moves?)
        state_board = read_board(webcam_device)  # FIXME do we need to pass device?
        if not "check if it's my turn":
            time.sleep(1)  # TODO async?
            time.sleep(29)  # XXX fill to 30s for testing docker volume mount
            continue  # next iteration

        state_board  # noqa trick linter for now - used in following actions
        "check if game is lost"  # --> surrender action loop
        "calculate next move"
        "make next move"
        "verify move was made correctly"  # stretch goal? --> may help debug high-level
        # feed back to Q at end of loop?


if __name__ == "__main__":

    # XXX
    import os
    print(os.listdir("/dev"))

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
