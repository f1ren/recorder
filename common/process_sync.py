import os

FLAG_STOP_FILE_NAME = 'flag_stop'
FLAG_START_FILE_NAME = 'flag_start'


def reset_signals():
    for filename in [FLAG_STOP_FILE_NAME, ] + [f'flag_{s}_ready' for s in ('video', 'audio')]:
        if os.path.exists(filename):
            os.remove(filename)


def should_stop():
    return os.path.isfile(FLAG_STOP_FILE_NAME)


def signal_stop():
    open(FLAG_STOP_FILE_NAME, 'a').close()
    if os.path.exists(FLAG_START_FILE_NAME):
        os.remove(FLAG_START_FILE_NAME)


def has_started():
    return os.path.isfile(FLAG_START_FILE_NAME)


def signal_start():
    open(FLAG_START_FILE_NAME, 'a').close()

