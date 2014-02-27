from flask import Blueprint
from flask import render_template
from flask import request, session, Response
from StringIO import StringIO
import time
import uuid

from utils import RESOLUTIONS, Config
from imgutils import get_image

streamer = Blueprint('streamer', __name__, template_folder='templates', static_folder='static')




@streamer.route('/stream.html', methods=['GET', 'POST'])
def home():
    """ Render page displaying all controls"""
    config = Config.get(session)
    if request.method == "POST":
        config.update(request, session)
    return render_template('stream.html', resolutions=RESOLUTIONS, config=config)

@streamer.route('/simple.html', methods=['GET'])
def show_simple_page():
    """ Display only the stream in lower resolution without any controls."""
    return render_template('simple.html', config=Config.get(session))

@streamer.route('/stream.mjpg')
def stream_cam():

    def getstream(config):
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

    config = Config.get(session)
    boundary = uuid.uuid4().hex
    headers = [('Content-Type', 'multipart/x-mixed-replace; boundary=--%s' % boundary)]
    return Response(getstream(config), headers=headers, direct_passthrough=True)
