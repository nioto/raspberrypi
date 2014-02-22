---
layout: index
title: PiCamStreamer
---

# PiCamStreamer

Create a mjpeg server for you Pi Camera module

Defines a [Blueprint](http://flask.pocoo.org/docs/blueprints/) to use under the micro web framework [Flask](http://flask.pocoo.org/) .

This project uses the [PiCamera interface](https://github.com/waveform80/picamera/).

Based on the code from [Simple mjpeg server](https://gist.github.com/n3wtron/4624820)

#### There are 2 modes:

1. Simple : only streaming
2. With controls : allow you to change resolution, view strem on grayscale, add timestamp on image, change quality of image (need PIL library)

Install dependancies

```bash
$ sudo apt-get install python-picamera
$ sudo apt-get install python-flask
$ sudo apt-get install python-imaging
```

Under [BSD license](https://raw.github.com/nioto/PiCamStreamer/master/LICENSE)


