from flask import Blueprint
from flask import render_template
from flask import request, session
from flask import Response
from StringIO import StringIO
import time
import uuid
from PIL import ImageOps, ImageFont, ImageDraw, Image
from datetime import datetime

streamer = Blueprint('streamer', __name__, template_folder='templates', static_folder='static')


class Resolution(object):
    id = 0
    values = ()

    def __init__(self, rid, values):
        self.id = rid
        self.values = values
        self.name = str(self.values)

    def __str__(self):
        return "Resolution=(%s, %s)" % (str(self.id), self.name)

RESOLUTIONS = [Resolution(1, (320, 240)), Resolution(2, (640, 480)), Resolution(3, (960, 720)), Resolution(4, (1280, 960))]

CONFIG_KEY_SESSION = "streamer.config_key"

class Config(object):
    resolution = RESOLUTIONS[0]
    grayscale = False
    insert_time = True
    quality = 70

    def __init__(self, http_request=None, resolution=RESOLUTIONS[1], grayscale=False, time=False, quality=70):
        if http_request is not None:
            index = int(http_request.values.get('resolution', 1))
            self.resolution = RESOLUTIONS[index-1]
            if http_request.values.get('grayscale', -1) >= 0:
                self.grayscale = True
            else:
                self.grayscale = False
            if http_request.values.get('time', -1) >= 0:
                self.insert_time = True
            else:
                self.insert_time = False
        else:
            self.resolution = resolution
            self.grayscale = grayscale
            self.time = time
            self.quality = time

    def __str__(self):
        return "Config (%s, grayscale=%s)" % (str(self.resolution), str(self.grayscale))

    def clear(self):
        self.resolution = RESOLUTIONS[0]
        self.grayscale = False
        self.insert_time = True
        self.quality = 70

    @staticmethod
    def get_config_from_req(r):
        if r.method == 'GET' and CONFIG_KEY_SESSION in session:
            config = Config.get_config_from_session()
        else:
            config = Config(r)
            session[CONFIG_KEY_SESSION] = config
        return config

    @staticmethod
    def get_config_from_session():
        return session[CONFIG_KEY_SESSION]

    @staticmethod
    def set_default_config():
        session[CONFIG_KEY_SESSION] = CONFIG_DEFAULT
        return session[CONFIG_KEY_SESSION]


CONFIG_DEFAULT = Config(None)

@streamer.route('/stream.html', methods=['GET', 'POST'])
def show_main_page():
    return render_template('stream.html', resolutions=RESOLUTIONS, config=Config.get_config_from_req(request))

@streamer.route('/simple.html', methods=['GET'])
def show_simple_page():
    return render_template('simple.html', config=Config.set_default_config())


@streamer.route('/stream.mjpg')
def stream_cam():
    boundary = uuid.uuid4().hex
    config = Config.get_config_from_req(request)

    def getimagestream():
        while True:
            tmp = StringIO()
            tmp.write('--%s\n' % boundary)
            tmp.write('Content-type=image/jpeg\n')
            img = get_image(config)
            tmp.write('Content-length= %s\n\n' % str(img.len))
            tmp.write(img.getvalue())
            tmp.write('\n\n')
            yield tmp.getvalue()
            time.sleep(1)
            tmp.close()
            img.close()

    headers = [('Content-Type', 'multipart/x-mixed-replace; boundary=--%s' % boundary)]
    return Response(getimagestream(), headers=headers, direct_passthrough=True)


try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 25)
except IOError:
    FONT = ImageFont.load_default()


def get_image(config):
    imgstr = None
    try:
        import picamera.PiCamera as PiCamera
        imgstr = get_image_from_picam(PiCamera(), config)
    except:
        imgstr = get_image_from_webcam(config)
    image = Image.fromstring("RGBA", config.resolution.values, imgstr)
    # Convert to RGB mode
    if image.mode != "RGB":
        image.convert("RGB")
    if config.insert_time:
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), datetime.today().strftime("%b %d %Y - %H.%M.%S"), fill=(255,255,255), font=FONT)
    if config.grayscale:
        image = ImageOps.grayscale(image)
    res = StringIO()
    image.save(res, 'JPEG', quality=config.quality)
    return res


def get_image_from_picam(cam, config):
    image = StringIO()
    try:
        cam.resolution = config.resolution.values
        cam.capture(image)
    finally:
        cam.close()
    return image.getvalue()

_is_init = False


def get_image_from_webcam(config):
    global _is_init
    import pygame
    import pygame.camera
    if not _is_init:
        pygame.init()
        pygame.camera.init()
        _is_init = True
    cam = pygame.camera.Camera("/dev/video0", config.resolution.values)
    cam.start()
    cam.get_image()  # skip, the 1st image webcam need initialization
    time.sleep(.3)  # let her initilize
    image = cam.get_image()
    res = pygame.image.tostring(image, "RGBA", False)
    cam.stop()
    del cam
    return res
