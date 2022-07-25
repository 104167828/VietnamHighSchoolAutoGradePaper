import json

from main import GetPoint, GetID
from flask import Flask, render_template, request, jsonify
import base64
from base64 import decode
from io import BytesIO
from PIL import Image
import cv2
from transform import detectPts
import imgProcess as pros
app = Flask(__name__)


@app.route('/')
def hello():
    """Renders a sample page."""
    return "'<img src= 'https://play-lh.googleusercontent.com/ZvMvaLTdYMrD6U1B3wPKL6siMYG8nSTEnzhLiMsH7QHwQXs3ZzSZuYh3_PTxoU5nKqU' alt='Flowers in Chania'>'"

@app.route('/check/')
def GetURL(method = ['GET','POST']):
    try:
        im = Image.open(BytesIO(base64.b64decode(request.form["Base64"])))
        im.save("test.jpg")
        AnsJSON = GetPoint("test.jpg")
        IdJson = GetID("test.jpg")
        IdJson["Answer"] = AnsJSON

    except cv2.error as e:
        print(e)
    return jsonify(IdJson)
if __name__ == '__main__':
    app.run()
