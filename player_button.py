import os
import random
import time
from subprocess import PIPE, Popen, STDOUT
import RPi.GPIO as GPIO

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')

def getVideos():
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            videos.append(os.path.join(directory, file))
    return videos


def playVideos():
    random.shuffle(videos)
    for video in videos:
        playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])
        playProcess.wait()

class Button():
    def __init__(self):
        self.pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isPressed(self):
        return not GPIO.input(self.pin)


class VideoPlayer():
    def __init__(self, playlist, button):
        self.playlist = playlist
        self.active = False
        self.process = None
        self.button = button
        

    def update(self):
        print(self.button.isPressed())


if __name__ == '__main__':
    videos = getVideos()
    button = Button()
    player = VideoPlayer(videos, button)
    while (True):
        player.update()
        # playVideos()
        time.sleep(0.3)
