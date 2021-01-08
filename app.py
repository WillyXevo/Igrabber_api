import flask
from flask import request, jsonify, json
import instaloader
from instaloader import Profile, LoginRequiredException
import base64

L = instaloader.Instaloader()

app = flask.Flask(__name__)

def e_url(s):
    ssb = s.encode("ascii") 

    base64_bytes = base64.b64encode(ssb) 
    base64_string = base64_bytes.decode("ascii") 
    
    strstr = base64_string.translate(str.maketrans('+/', '-_'))
    return strstr.rstrip('=') 

def d_url(s):
    strstr = s.translate(str.maketrans('+/', '-_'))
    le = len(s) + 10
    pad_right = strstr.ljust(le, '=')
    ret = base64.b64decode(pad_right).decode('utf-8')
    return ret

def get_link(p):
    if p.is_video:
        display = ''
        if hasattr(p, 'display_url'):
            display = p.display_url
        else:
            display = p.url
        return {'is_video':"true", 'display':display, 'url':p.video_url}
    else:
        display = ''
        if hasattr(p, 'display_url'):
            display = p.display_url
        else:
            display = p.url
        return {'is_video':"false", 'url':display}


def get_post(SHORTCODE):
    try:
        post = instaloader.Post.from_shortcode(L.context, SHORTCODE)
        typename = post.typename

        url_arr = []

        if typename=="GraphSidecar":
            for p in post.get_sidecar_nodes():
                url_arr.append(get_link(p))
        else:
            url_arr.append(get_link(post))
         
        jsona = json.dumps(url_arr)
        return jsona
    except:
        return ""

def cek_login(USER, PASS):
    USER = d_url(USER)
    PASS = d_url(PASS)
    try:
        L.login(USER, PASS) 
        a = L.test_login();
        return a
    except:
        return "false"

def get_story(USERNAME):
    try:
        # if (cek_login(USER, PASS) != "false"):
        #     profile = Profile.from_username(L.context, USERNAME)
        #     proID = profile.userid
        #     url_arr = []
        #     for story in L.get_stories(userids=[proID]):
        #         for item in story.get_items():
        #             url_arr.append(get_link(item))
        #     jsona = json.dumps(url_arr)
        # else:
        #     jsona = "false login"
        profile = Profile.from_username(L.context, USERNAME)
        proID = profile.userid
        url_arr = []
        for story in L.get_stories(userids=[proID]):
            for item in story.get_items():
                url_arr.append(get_link(item))
        jsona = json.dumps(url_arr)
        return jsona
    except LoginRequiredException as e:
        return "false"
    except:
        return "false"

def get_highlight(USERNAME):
    try:
        profile = Profile.from_username(L.context, USERNAME)
        proID = profile.userid
        url_arr = []
        for highlight  in L.get_highlights(proID):
            for item in highlight.get_items():
                url_arr.append(get_link(item))

        jsona = json.dumps(url_arr)
        return jsona
    except LoginRequiredException as e:
        return "false"
    except:
        return "false"

def test(a):
    return a


@app.route('/', methods=['GET'])
def home():
    return "<h1>igrabber</h1><p>This site is a prototype API for igrabber.</p>"

@app.route('/t/<link_url>', methods=['GET'])
def t(link_url):
    return test(link_url)

@app.route('/gp/<link_url>', methods=['GET'])
def gp(link_url):
    return get_post(link_url)

@app.route('/ck_log/<u>/<p>', methods=['GET'])
def clog(u, p):
    return cek_login(u, p)

@app.route('/gs/<u>', methods=['GET'])
def gs(u):
    return get_story(u)

@app.route('/gh/<u>', methods=['GET'])
def gh(u):
    return get_highlight(u)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

