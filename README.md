# Igrabber_api
_The scraper uses the awesome library [Instaloader](https://instaloader.github.io/) to get data from instagram._
_This doesn't use the instagram API because it is slow and has other limitations. Please don't run multiples instances of this scraper at same time from same device._
_this is an open API so you don't need a key to access, simply clone this repositoory to your server and run it._
_you can use this API for mobile developmet to make a online reading manga application._

## Features
- get url source from instagram post

## Installation

OS X & Linux:

Open terminal

1. ``` git clone  https://github.com/SatuSembilanDua/igrabber_api```
2. ``` cd igrabber_api/ ```
3. ``` pip install -r requirements.txt ```

Windows:

Download python [here](https://www.python.org/downloads/)
1. ```Download [https://github.com/SatuSembilanDua/igrabber_api/archive/master.zip](https://github.com/SatuSembilanDua/igrabber_api/archive/master.zip) ```
2. ``` Extract to a folder```
3. ``` Open cmd and navigate to the folder you just put the extractor on.```
4. ``` pip install -r requirements.txt ```

## Usage example
```
python app.py 
```
wait until it's ready
```
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 100-432-952
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

open browser and then open 
```http://127.0.0.1:5000```
to get url from post's shortcode :
```http://127.0.0.1:5000/gp/<shortcode>```
example you will download image post from ```https://www.instagram.com/p/CJtAAjPA2Kd/``` the shortcode is ```CJtAAjPA2Kd``` then change url to ```http://127.0.0.1:5000/gp/CJtAAjPA2Kd```
you will get result :
```
[
  {
    "is_video": "false",
    "url": "https://scontent-cgk1-2.cdninstagram.com/v/t51.2885-15/e35/135825776_853475338557959_158294133343559136_n.jpg?_nc_ht=scontent-cgk1-2.cdninstagram.com&_nc_cat=1&_nc_ohc=EXWfQVIU2RgAX9VLM2M&tp=1&oh=3253004c169e2bb49726a87d91e4f357&oe=601ECDE8"
  }
]
```