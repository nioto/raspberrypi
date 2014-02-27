from flask import Flask, request
from flask import render_template
from flask import redirect, url_for


app = Flask(__name__, template_folder='picamstreamer/templates', static_folder='picamstreamer/static')

from picamstreamer import streamer
app.register_blueprint(streamer)

from picamstreamer import RESOLUTIONS, Config


app.config.update(
    SECRET_KEY="098765432109876",
    SESSION_COOKIE_NAME = "my_cookie"
)

@app.route('/', methods=['GET'])
def index():
    return redirect( url_for('streamer.home') )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
