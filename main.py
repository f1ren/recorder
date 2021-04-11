import sys

from audio.microphone import audio_capture
from common.process_sync import reset_signals, signal_stop, has_started, signal_start
from video.camera import video_capture


def main():
    if not has_started():
        reset_signals()
        signal_start()

    if sys.argv[1] == 'mic':
        audio_capture()
    elif sys.argv[1] == 'cam':
        video_capture()
    else:
        print('Must have mic or cam argument')
        exit(1)

    signal_stop()


if __name__ == '__main__':
    main()
