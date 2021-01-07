import flask
from flask import request, jsonify, json
import instaloader

L = instaloader.Instaloader()

app = flask.Flask(__name__)

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

def get_post2(SHORTCODE, u, p):
    try:
        L.login(u, p)
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

def test(a):
    return a


@app.route('/', methods=['GET'])
def home():
    return "<h1>igrabber</h1><p>This site is a prototype API for igrabber.</p>"

@app.route('/gp/<link_url>', methods=['GET'])
def gp(link_url):
    return get_post(link_url)

@app.route('/gp2/<link_url>/<u>/<p>', methods=['GET'])
def gp2(link_url):
    return get_post2(link_url, u, p)

@app.route('/t/<link_url>', methods=['GET'])
def t(link_url):
    return test(link_url)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

