import base64
# from PIL import Image
# from io import BytesIO
from util import callAPI, encode_image_from_file
import math
import time
import cv2


def getObjectsThenLabel(image_file):
    print('== api fisrt call', time.time())
    image_base64 = encode_image_from_file(image_file)
    # image_pil = Image.open(image_file)
    image_cv = cv2.imread(image_file)

    # get location of each objects
    response = callAPI(image_base64, 'LOC')

    obj_loc_list = response['responses'][0]["localizedObjectAnnotations"]

    print('== api fisrt call end', time.time())

    # w, h = image_pil.size
    h, w, _ = image_cv.shape

    res = {'objectNum': len(obj_loc_list), 'objectList': []}
    for obj_loc in obj_loc_list:
        print('==== loop one start', time.time())
        vx_list = obj_loc["boundingPoly"]["normalizedVertices"]
        ux = int(math.floor(vx_list[0]['x'] * w))
        uy = int(math.floor(vx_list[0]['y'] * h))
        dx = int(math.floor(vx_list[2]['x'] * w))
        dy = int(math.floor(vx_list[2]['y'] * h))

        # image_pil_single_obj = image_pil.crop((ux, uy, dx, dy))
        image_cv_single_obj = image_cv[uy:dy, ux:dx]

        # output = BytesIO()
        # image_pil_single_obj.save(output, format='JPEG')
        # _image_pil_single_obj = output.getvalue()
        # image_base64_single_obj = base64.b64encode(_image_pil_single_obj)

        # im_arr: image in Numpy one-dim array format.
        _, image_cv_single_obj_arr = cv2.imencode('.jpg', image_cv_single_obj)
        image_cv_single_obj_bytes = image_cv_single_obj_arr.tobytes()
        image_base64_single_obj = base64.b64encode(image_cv_single_obj_bytes)

        print('====== get label start', time.time())
        label_list = getLabel(image_base64_single_obj)
        print('====== get label end', time.time())
        obj_label = {'name': label_list, 'loc': [ux, uy, dx, dy]}
        res['objectList'].append(obj_label)

        print('==== one loop end', time.time())

    return res


def getLabel(image_base64):
    # get label of a single object

    print('======== in loop call api', time.time())
    response = callAPI(image_base64, 'LABEL')
    print('======== in loop call api end', time.time())
    labelList = response['responses'][0]["labelAnnotations"]
    res = []
    for label in labelList:
        if float(label['score']) >= 0.9:
            res.append(label["description"])
        if float(label['score']) < 0.9:
            break
    return res


print('start', time.time())
a = getObjectsThenLabel(
    '/opt/mycroft/skills/sandbox-git-skill/photo/multi.jpeg')
print(a)
print('end', time.time())
