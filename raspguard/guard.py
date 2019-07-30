import argparse
import datetime
import imutils
import time
import telegram
import cv2
import os

from raspguard import settings

from moviepy.editor import ImageSequenceClip
from imutils.video import VideoStream


class RaspGuard:

    def __init__(self):
        self.is_recording = False
        self.frames_to_save = []
        self.vs = VideoStream(src=0).start()
        self.bot = telegram.Bot(token=settings.TG_BOT_API_KEY)
        time.sleep(2.0)

    def run(self):
        # loop over the frames of the video
        while True:
            # grab the current frame 
            frame = self.vs.read()

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # threshold it
            thresh_ = 255.0 / 100 * (100 - settings.SENSITIVITY)
            _, thresh = cv2.threshold(gray, thresh_, 255, cv2.THRESH_BINARY)

            # erode + dilate to make contours better
            thresh = cv2.erode(thresh, None, iterations=2)
            thresh = cv2.dilate(thresh, None, iterations=10)

            # find contours
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            self.detect_light(contours, frame)

            key = cv2.waitKey(1) & 0xFF 
            if key == ord("q"):
                break
        
        self.stop()

    def detect_light(self, contours, frame):
        if any([cv2.contourArea(c) > settings.MIN_CONTOUR for c in contours]):
            self.is_recording = True
            self.frames_to_save.append(frame)

            if len(self.frames_to_save) >= settings.MAX_FRAMES:
                self.stop_recording()
                path = self.write_gif()
                self.send_gif(path)
            
            print('is recording')
            time.sleep(1.0 / settings.GIF_FPS)
        else:
            if self.is_recording:
                path = self.write_gif()
                self.send_gif(path)

            self.stop_recording()

    def stop_recording(self):
        self.is_recording = False
        self.frames_to_save = []

    def gif_path(self):
        now = datetime.datetime.now()
        if not os.path.exists(settings.GIF_FOLDER):
            os.mkdir(settings.GIF_FOLDER)

        return os.path.join(settings.GIF_FOLDER, '{}.gif'.format(now.strftime(settings.DATETIME_FORMAT)))
            
    def write_gif(self):
        filename = self.gif_path()
        clip = ImageSequenceClip(self.frames_to_save, fps=2)
        clip.write_gif(filename, fps=2)
        return filename

    def send_gif(self, path, caption=None):
        if caption is None:
            caption = os.path.basename(path)

        try:
            self.bot.send_animation(settings.TG_CHANNEL_ID, open(path, 'rb'), caption=caption)
        except:
            self.bot.send_message(settings.TG_CHANNEL_ID, 'Message sending failed. See {} for GIF animation'.format(path))

    def stop(self):
        self.vs.stop()
        cv2.destroyAllWindows()
