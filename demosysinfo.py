from flask import Flask, request
from flask import render_template
from flask import redirect, url_for

from pisysinfo import pisysinfo


app = Flask(__name__, template_folder='pisysinfo/templates', static_folder='pisysinfo/static')

app.register_blueprint(pisysinfo)


app.config.update(
    SECRET_KEY="098765432109876",
    SESSION_COOKIE_NAME = "my_cookie"
)

@app.route('/', methods=['GET'])
def index():
    return redirect( url_for('pisysinfo.home') )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
