from main import GetPoint, GetID
from flask import Flask, request, jsonify
import base64
import json
from io import BytesIO
from PIL import Image
import cv2

app = Flask(__name__)

@app.route('/')
def hello():
    """Renders a sample page."""
    return "'<img src= 'https://play-lh.googleusercontent.com/ZvMvaLTdYMrD6U1B3wPKL6siMYG8nSTEnzhLiMsH7QHwQXs3ZzSZuYh3_PTxoU5nKqU' alt='Flowers in Chania'>'"

@app.route('/check/', methods=['GET', 'POST'])
def GetURL(methods = ['GET','POST']):
    try:
        base64_modify = ""
        json_income = request.data
        json_modify = json.loads(json_income)
        base64_modify = json_modify["string"]
        im = Image.open(BytesIO(base64.b64decode(base64_modify)))
        im.save("test.jpg")
        AnsJSON = GetPoint("test.jpg")
        IdJson = GetID("test.jpg")
        IdJson["Answer"] = AnsJSON
    except cv2.error as e:
        print(e)
    return IdJson
if __name__ == '__main__':
    app.run()
