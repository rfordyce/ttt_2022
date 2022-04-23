import time

# import opencv  # for board reading - should this be trained or ugly dynamic?
# import redis  # for distributed queue

# should this use a display queue and thread?
#   practically to prefer over gross python logging
#   otherwise feed into redis queue --> display on API/UI via socket?..


def read_board():
    pass


def surrender_loop():
    while True:
        if "check if board is cleared":
            break
        # should this explicitly drive arm to fixed positions?
        "clear surrender action series"


def main():
    while True:
        # read Q (redis)? (may have explicit moves?)
        state_board = "check board state"
        if not "check if it's my turn":
            time.sleep(1)  # TODO async?
            continue  # next iteration

        state_board  # noqa trick linter for now - used in following actions
        "check if game is lost"  # --> surrender action loop
        "calculate next move"
        "make next move"
        "verify move was made correctly"  # stretch goal? --> may help debug high-level
        # feed back to Q at end of loop?


if __name__ == "__main__":
    # argparser
    # discover camera device?
    main()
