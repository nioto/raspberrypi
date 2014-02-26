import threading
import picamera


# Define a class to acces PiCamera using locks to avoid thread access
class __Camera(object):
    """ Define a class to avoid mutiple access to the Picamera on the same time ,
    in a multi threading environment. Only supports capture method
    Just use the CAMERA obect
    """
    def __init__(self):
        self.lock = threading.Lock()

    def setCopyright(self, copyright=None):
        self.copyright = copyright

    def capture(self, file=None, resolution=(1280, 720), quality=70):
        with self.lock:
            with picamera.PiCamera() as camera:
                camera.exif_tags['IFD0.Copyright'] = self.copyright
                camera.resolution = self.resolution
                camera.capture(file, 'jpeg', quality=quality)



__CAMERA = __Camera()


def capture(file=None, resolution=(1280, 720), quality=70):
    __CAMERA.capture(file, resolution, quality)
