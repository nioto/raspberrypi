from flask import Blueprint
from flask import render_template

import psutil
import os
import time
from datetime import timedelta, datetime


pisysinfo = Blueprint('pisysinfo', __name__, template_folder='templates', static_folder='static')


import subprocess, re


# bug in filesizeformat in jinja2
# added corrected version
def do_filesizeformat(value, binary=False):
    """Format the value like a 'human-readable' file size (i.e. 13 kB,
    4.1 MB, 102 Bytes, etc). Per default decimal prefixes are used (Mega,
    Giga, etc.), if the second parameter is set to `True` the binary
    prefixes are used (Mebi, Gibi).
    """
    bytes = float(value)
    base = binary and 1024 or 1000
    prefixes = [
        (binary and 'KiB' or 'kB'),
        (binary and 'MiB' or 'MB'),
        (binary and 'GiB' or 'GB'),
        (binary and 'TiB' or 'TB'),
        (binary and 'PiB' or 'PB'),
        (binary and 'EiB' or 'EB'),
        (binary and 'ZiB' or 'ZB'),
        (binary and 'YiB' or 'YB')
    ]
    if bytes == 1:
        return '1 Byte'
    elif bytes < base:
        return '%d Bytes' % bytes
    else:
        for i, prefix in enumerate(prefixes):
            unit = base ** (i + 2)
            if bytes < unit:
                return '%.1f %s' % ((base * bytes / unit), prefix)
        return '%.1f %s' % ((base * bytes / unit), prefix)


def get_ipv4_address(localhost=False):
    """
    Returns IP address(es) of current machine.
    :return:
    """
    p = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    ifc_resp = p.communicate()
    patt = re.compile(r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    resp = patt.findall(ifc_resp[0])
    if not localhost:
        resp = [ip for ip in resp if not ip.startswith("127.0") ]
    return resp

IPs = get_ipv4_address(localhost=False)

# release
def getrelease():
    """
     Read the name of the release  find in /etc/os-release  under the name PRETTY_NAME
    """
    with open('/etc/os-release', 'r') as file:
        for line in file:
            if line.startswith('PRETTY_NAME='):
                return line[13:-2]
    return "Unknown"

RELEASE = getrelease()

def get_memory_usage():
    """
    Returns the memory information of the host.
    :return:  (total, used, free)
    """
    p = subprocess.Popen(["free", "-b"], stdout=subprocess.PIPE)
    ifc_resp = p.communicate()
    patt = re.compile(r'Mem:\s*([^\s]*)\s*([^\s]*)\s*([^\s]*)')
    resp = patt.findall(ifc_resp[0])
    l = [ int(v) for v in resp[0]]
    return l

def delta(time_from):
    tmp = timedelta( seconds= time.time()-time_from )
    h = tmp.seconds/3600
    min = (tmp.seconds - 3600 * h) / 60
    params=()
    stformat = "{0} day(s), {1} hour(s), {2} minutes, {3} seconds."
    if tmp.days == 0:
        if h == 0:
            stformat = "{0} minutes, {1} seconds."
            params = ( min, tmp.seconds % 60 )
        else:
            stformat = "{0} hour(s), {1} minutes, {2} seconds."
            params = ( h, min, tmp.seconds % 60 )
    else :
        stformat = "{0} day(s), {1} hour(s), {2} minutes, {3} seconds."
        params = ( tmp.days, h, min, tmp.seconds % 60 )
    return stformat.format( *params )


@pisysinfo.route('/', methods=['GET'])
def home():
    """ Render page displaying all informations"""
    data = dict()
    # date of last boot
    data['host_up_since'] = delta(psutil.BOOT_TIME)
    # program launch time
    p = psutil.Process(os.getpid())
    data['prog_up_since'] = delta(p.create_time)
    # Ips
    data['ips'] = IPs
    # OS
    data['osname'] = RELEASE
    data['hostname'] = os.uname()[1]
    # disk utilisation
    disks=[]
    for dp in psutil.disk_partitions():
        p=dict()
        p["device"]=dp.device
        p["mountpoint"]=dp.mountpoint
        p["fstype"]=dp.fstype
        tmp = psutil.disk_usage(p["mountpoint"])
        p["ddtotal"]=do_filesizeformat(tmp.total)
        p["ddpercent"]= 0.1 * int( 1000 * tmp.used / tmp.total )
        p["ddfree"]=do_filesizeformat(tmp.free)
        disks.append( p )
    data['partitions']=disks
    # memory usage
    tmp =get_memory_usage()
    data['memtotal'] = do_filesizeformat( tmp[0] )
    data['mempercent'] = .1 * ( 1000 * tmp[1] / tmp[0] )
    return render_template('info.html', data = data)


if __name__ == '__main__':
    #global pisysinfo
    from flask import Flask
    app = Flask(__name__)
    #, template_folder='pisysinfo/templates', static_folder='pisysinfo/static')
    app.register_blueprint(pisysinfo)
    app.config.update(
        SECRET_KEY="098765432109876",
        SESSION_COOKIE_NAME = "my_cookie"
    )
    @app.route('/', methods=['GET'])
    def index():
        return redirect( url_for('pisysinfo.home') )
    app.run(host='0.0.0.0', port=3000, debug=True)
