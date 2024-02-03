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

class ScreenBacklight():
    def __init__(self):
        # Need to set the initial value before doing anything. No idea why.
        self.turnOff()

    def turnOn(self):
        os.system("sudo bash -c 'echo 0 > /sys/class/backlight/rpi_backlight/bl_power'")

    def turnOff(self):
        os.system("sudo bash -c 'echo 1 > /sys/class/backlight/rpi_backlight/bl_power'")


class VideoPlayer():
    def __init__(self, playlist, button, backlight: ScreenBacklight):
        self.playlist = playlist
        self.active = False
        self.process = None
        self.button = button
        self.backlight = backlight

        self.isButtonPressed = None
      

    def update(self):
        pressed = self.button.isPressed()
        if pressed != self.isButtonPressed:
            if pressed:
                self.onButtonPressed()
            self.isButtonPressed = pressed


    def onButtonPressed(self):
        self.active = not self.active
        if self.active:
            self.onActivate()
        else:
            self.onDeactivate()


    def onActivate(self):
        print("activate!")
        self.backlight.turnOn()

    def onDeactivate(self):
        print("deactivate!")
        self.backlight.turnOff()
        

if __name__ == '__main__':
    videos = getVideos()
    button = Button()
    backlight = ScreenBacklight()
    player = VideoPlayer(videos, button, backlight)
    while (True):
        player.update()
        # playVideos()
        time.sleep(0.3)
