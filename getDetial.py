
from util import callAPI, encode_image_from_file
from webcolors import CSS3_HEX_TO_NAMES
from webcolors import hex_to_rgb
from scipy.spatial import KDTree
import time


def getRGBValues():
    css3_db = CSS3_HEX_TO_NAMES

    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    return rgb_values, names


def getColorNameFromRGB(rgb_tuple, rgb_values, names):

    # a dictionary of all the hex and their respective names in css3

    kdt_db = KDTree(rgb_values)
    _, index = kdt_db.query(rgb_tuple)
    return names[index]


def extractInfo(response, responseKey, resNum, res, resKey):
    try:
        extractList = response[responseKey]
    except:
        print('no ' + responseKey)
    
    for i in range(resNum):
        try:
            res[resKey].append(extractList[i]["description"])
        except:
            print('no enough ' + resKey)

def getDetial(image_file):

    image_base64 = encode_image_from_file(image_file)
    response = callAPI(image_base64)

    res = {'objectLabel': [], 'objectLogo': [],
           'objectText': [], 'objectColor': []}
    
    extractInfo(response['responses'][0], "labelAnnotations", 3, res, 'objectLabel')
    extractInfo(response['responses'][0], "logoAnnotations", 3, res, 'objectLogo')

    # for label in labelList:
    #     if float(label['score']) >= 0.85:
    #         res['objectLabel'].append(label["description"])
    #     if float(label['score']) < 0.85:
    #         break

    # logoList = response['responses'][0]["logoAnnotations"]
    # for logo in logoList:
    #     if float(logo['score']) >= 0.8:
    #         res['objectLogo'].append(logo["description"])
    #     if float(logo['score']) < 0.8:
    #         break

    textList = response['responses'][0]["textAnnotations"]
    try:
        res['objectText']= textList[0]["description"].split("\n")
    except:
        print('no enough objectText')

    colorList = response['responses'][0]["imagePropertiesAnnotation"]["dominantColors"]["colors"]
    rgb_values, names = getRGBValues()
    # for color in colorList:
    #     if float(color['score']) >= 0.1:
    #         rgbList = [color["color"]['red'], color["color"]
    #                    ['green'], color["color"]['blue']]
    #         res['objectColor'].append(
    #             {'colorName': getColorNameFromRGB(tuple(rgbList), rgb_values, names),
    #              'rgb': rgbList
    #              }
    #         )
    #     if float(color['score']) < 0.1:
    #         break
    for i in range(3):
        try:
            color = colorList[i]
            rgbList = [color["color"]['red'], color["color"]
                       ['green'], color["color"]['blue']]
            res['objectColor'].append(
                {'colorName': getColorNameFromRGB(tuple(rgbList), rgb_values, names),
                 'rgb': rgbList
                 }
            )
        except:
            print('no enough objectColor')

    return res


print(time.time())
a = getDetial('/opt/mycroft/skills/sandbox-git-skill/photo/multi.jpeg')
print(a)
print(time.time())
