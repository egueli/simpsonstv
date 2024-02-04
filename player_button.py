import os
import random
import time
import RPi.GPIO as GPIO
from omxplayer.player import OMXPlayer

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
        self.player: OMXPlayer = None
        self.button = button
        self.backlight = backlight

        self.isButtonPressed = None
      

    def update(self):
        self.updateButtonState()
        self.updatePlayerState()

    def updateButtonState(self):
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

        self.stopVideoPlayer()
        self.startVideoPlayer()

    def onDeactivate(self):
        print("deactivate!")
        self.backlight.turnOff()
        self.stopVideoPlayer()
        
    def stopVideoPlayer(self):
        if self.player:
            self.player.quit()
        self.player = None

    def startVideoPlayer(self):
        video = random.choice(self.playlist)
        self.player = OMXPlayer(video, args=['--no-osd', '--aspect-mode', 'fill'])
        # it takes about this long for omxplayer to warm up and start displaying a picture.
        # Before that, calls to OMXPlayer.playback_status() will hang.
        time.sleep(1.5)

    def updatePlayerState(self):
        state = None
        if self.player is not None:
            state = self.player.playback_status()
        
        print(f'updatePlayerState {state}')

if __name__ == '__main__':
    videos = getVideos()
    button = Button()
    backlight = ScreenBacklight()
    player = VideoPlayer(videos, button, backlight)
    while (True):
        player.update()
        # playVideos()
        time.sleep(0.3)
