#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import ImageOps, ImageFont, ImageDraw, Image
import io
import time
from datetime import datetime
from StringIO import StringIO
import threading
from picamutils import capture

# Load default font to draw time on stream
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif-Bold.ttf", 20)
except IOError:
    FONT = ImageFont.load_default()

__use_PiCamera= True
try:
    from picamera import PiCamera
except ImportError:
    __use_PiCamera = False

# Init pygame camera if necessary
if not __use_PiCamera:
    import pygame
    import pygame.camera
    pygame.init()
    pygame.camera.init()


def get_image(config):
    """ Retrieve an image from the webcam (or picam) as a StringIO """
    if __use_PiCamera:
        image = get_image_from_picam(config)
    else:
        image = get_image_from_webcam(config)
    # Convert to RGB mode
    if image.mode != "RGB":
        image.convert("RGB")
    if config.showtime:
        d = ImageDraw.Draw(image)
        d.text((0, 0), datetime.today().strftime("%b %d %Y - %H.%M.%S"), fill=(255,255,255), font=FONT)
    if config.grayscale:
        image = ImageOps.grayscale(image)
    res = StringIO()
    image.save(res, 'JPEG', quality=config.quality)
    return res


def get_image_from_picam(config):
    """ Use PiCamera module to get an image """
    data = io.BytesIO()
    capture(image, config.resolution.values, quality=config.quality)
    data.seek(0)
    return Image.open(data)


def get_image_from_webcam(config):
    """ Use Pygame.Camera module to get an image from webcam on /dev/video0 """
    cam = pygame.camera.Camera("/dev/video0", config.resolution.values, "RGB")
    cam.start()
    cam.get_image()  # skip, the 1st image, some webcam need initialization to get a correct image
    time.sleep(.1)  # let her initilize
    image = cam.get_image()
    cam.stop()
    del cam
    return convert_surface( image, config.resolution.values )

def convert_surface(image, resolution):
    """  Convert a Surface object (from pygame)  to an Image object ( from PIL )"""
    string = pygame.image.tostring(image, "RGB", False)
    return Image.fromstring("RGB", resolution, string)
