import flask
from flask import request, jsonify, json
import instaloader
from instaloader import Profile, LoginRequiredException
import base64, re
from requests import get, post

uag = "Mozilla/5.0 (Linux; Android 9; SM-A102U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Instagram 155.0.0.37.107 Android (28/9; 320dpi; 720x1468; samsung; SM-A102U; a10e; exynos7885; en_US; 239490550)"
headers = {
	'User-Agent': uag
}
L = instaloader.Instaloader(user_agent=uag)

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

def GraphImage(sm):
	ds = sm["display_resources"]
	src = ds[len(ds)-1]["src"]
	return {"is_video":"false", "url":src}

def GraphVideo(sm):
	ds = sm["video_url"]
	return {"is_video":"true", "url":ds}

def gp_request(SHORTCODE):
	url = f"https://www.instagram.com/p/{SHORTCODE}/"
	itg = get(url, headers=headers).text

	rexcmd = r"window\.\_sharedData \= (.*?);<\/script\>"
	matches = re.search(rexcmd, itg)
	x = []
	if matches:
		x = matches.group(1)
		y = json.loads(x)
		__typename = y["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]
		ret = []
		if __typename == "GraphImage":
			sm = y["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
			ret.append(GraphImage(sm))
		elif __typename == "GraphVideo":
			sm = y["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
			ret.append(GraphVideo(sm))
		elif __typename == "GraphSidecar":
			edge = y["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
			for e in edge:
				typename = e["node"]["__typename"]
				sm = e["node"]
				if typename == "GraphVideo":
					ret.append(GraphVideo(sm))
				else:
					ret.append(GraphImage(sm))
		return json.dumps(ret)
	else:
		return ""


def gp_instloader(SHORTCODE):
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

def gp_heroku(SHORTCODE):
	url = f"https://instcoba.herokuapp.com/gp/{SHORTCODE}/"
	itg = get(url, headers=headers).json()
	return itg

def get_post(SHORTCODE):
	ret = gp_instloader(SHORTCODE)
	if ret == "" :
		ret = gp_request(SHORTCODE)
		if ret == "":
			ret = gp_heroku(SHORTCODE)
			print("Using Heroku")
			return ret
		else:
			print("Using Requests")
			return ret
	else:
		print("Using Instaloader")
		return ret

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

