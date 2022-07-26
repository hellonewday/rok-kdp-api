from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
import cv2
import easyocr
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

reader = easyocr.Reader(['vi', 'en'])

"""
        Parameters to get region in the screen.
 """
# ID
ID_X = 415
ID_Y = 60
ID_W = 150
ID_H = 38
# Name
NAME_X = 305
NAME_Y = 90
NAME_W = 310
NAME_H = 40
# POWER - Apply blur
POWER_X = 500
POWER_Y = 170
POWER_W = 150
POWER_H = 40

# KILL POINTS
KILL_X = 30
KILL_Y = 150
KILL_W = 330
KILL_H = 200

# PREKVK
PRE_X = 800
PRE_Y = 250
PRE_W = 250
PRE_H = 100

## Resize width & height.
shrink_width = 850
shrink_height = 350

shrink_mini_width = 550
shrink_mini_height = 350

shrink_large_width = 1200
shrink_large_height = 800

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def extractInformation(imgUrl, shrink_w, shrink_h, x, y, w, h, apply_blur=False):
    def preprocess_overall_profile(sw, sh, profile):
        gray_img = cv2.cvtColor(profile, cv2.COLOR_BGR2GRAY)
        thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(
            thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if(w >= profile.shape[0] / 2 and h >= profile.shape[1] / 4):
                cv2.rectangle(profile, (x, y), (x + w, y + h),
                              (36, 255, 12), 3)
                new_profile = profile[y:y+h, x:x+w]
                new_profile = cv2.resize(new_profile, (sw, sh))
        return new_profile
    profile = cv2.imread(imgUrl)
    preprocess_img = preprocess_overall_profile(shrink_w, shrink_h, profile)
    cv2.rectangle(preprocess_img, (x, y), (x + w, y + h), (36, 255, 12), 3)
    id_image = preprocess_img[y:y+h, x:x+w]
    if apply_blur == True:
        id_image = cv2.blur(id_image, (3, 3))
    id_image = cv2.cvtColor(id_image, cv2.COLOR_BGR2GRAY)
    id_image = cv2.threshold(
        id_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return id_image


def production_api(profileUrl, infoUrl, preUrl):

    powerImage = extractInformation(
        profileUrl, shrink_width, shrink_height, POWER_X, POWER_Y, POWER_W, POWER_H, True)
    power = reader.readtext(powerImage)[0][1]

    idImage = extractInformation(
        profileUrl, shrink_width, shrink_height, ID_X, ID_Y, ID_W, ID_H, False)
    ID = reader.readtext(idImage)[0][1]

    nameImage = extractInformation(
        profileUrl, shrink_width, shrink_height, NAME_X, NAME_Y, NAME_W, NAME_H, False)
    name = reader.readtext(nameImage)[0][1]

    killpointImage = extractInformation(
        infoUrl, shrink_mini_width, shrink_mini_height, KILL_X, KILL_Y, KILL_W, KILL_H, False)
    killPointData = reader.readtext(killpointImage)
    killPoints = []
    for killPoint in killPointData:
        killPoints.append(killPoint[1])

    prekvkImage = extractInformation(
        preUrl, shrink_large_width, shrink_large_height, PRE_X, PRE_Y, PRE_W, PRE_H, False)
    prekvk = reader.readtext(prekvkImage)[0][1]

    return ID, name, power, killPoints, prekvk


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/uploads', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        profile = request.files["profile"]
        info = request.files["info"]
        pre = request.files["pre"]
        if profile and allowed_file(profile.filename):
            profileName = secure_filename(profile.filename)
            profile_path = os.path.join("tmp", profileName)
            profile.save(profile_path)

        if info and allowed_file(info.filename):
            infoName = secure_filename(info.filename)
            info_path = os.path.join("tmp", infoName)
            info.save(info_path)

        if pre and allowed_file(pre.filename):
            preName = secure_filename(pre.filename)
            pre_path = os.path.join("tmp", preName)
            pre.save(pre_path)

        extract_result = production_api(profile_path, info_path, pre_path)
        print("Complete extracting result")
        jsonResult = {
            "Id": extract_result[0],
            "Name": extract_result[1],
            "Power": extract_result[2],
            "Kill points": extract_result[3],
            "Pre-kvk points": extract_result[4]
        }
        return jsonify(jsonResult)
    else:
        return jsonify({"message": "Wrong method"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")