#!/usr/bin/env python
# -*- coding: utf-8 -*-


# String to use as key in sesion stroage for Config
CONFIG_KEY_SESSION = "streamer.config_key"

class Resolution(object):
    """ Defines a image resolution for displaying streaming """
    id = 0
    values = ()

    def __init__(self, rid, values):
        self.id = rid
        self.values = values
        self.name = str(self.values)

    def __str__(self):
        return "Resolution=({0}, {1})".format( str(self.id), self.name )

# List all available resolutions
RESOLUTIONS = [Resolution(1, (320, 240)), Resolution(2, (640, 480)), Resolution(3, (960, 720)), Resolution(4, (1280, 960))]

# Default resolution to use in Simple streamer
DEFAULT_RESOLUTION =  RESOLUTIONS[0]


class Config(object):
    """ Configuration class, contains informations on what user want to see (resolution, time, color/grayscale...)."""

    def __init__(self):
        self.resolution = DEFAULT_RESOLUTION
        self.grayscale = False
        self.showtime = True
        self.quality = 70

    def update(self, http_request,session):
        """ Update configuration from a POST request ."""
        index = int(http_request.values.get('resolution', 1))
        self.resolution = RESOLUTIONS[index-1]
        if http_request.values.get('grayscale', -1) >= 0:
            self.grayscale = True
        else:
            self.grayscale = False
        if http_request.values.get('showtime', -1) >= 0:
            self.showtime = True
        else:
            self.showtime = False
#        session[CONFIG_KEY_SESSION]=self

    def __str__(self):
        return "Config ( {0}, grayscale={1}, time={2}, quality={3})".format(str(self.resolution), str(self.grayscale), str(self.showtime), str(self.quality))

    def clear(self):
        self.resolution = DEFAULT_RESOLUTION
        self.grayscale = False
        self.showtime = True
        self.quality = 70

    @staticmethod
    def get(session):
        if CONFIG_KEY_SESSION not in session:
            session[CONFIG_KEY_SESSION] = Config()
        return  session[CONFIG_KEY_SESSION]

