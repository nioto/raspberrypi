from flask import Flask, request, session
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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("test.html", resolutions=RESOLUTIONS, config=Config.get_config_from_req(request))


@app.route('/st')
def test_redirect():
    return redirect( url_for('streamer.show_main_page') )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)