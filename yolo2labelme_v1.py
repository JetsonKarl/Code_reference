'''
Description：朱月明写的yolo转labelme读取格式代码
'''
from asyncio.windows_events import NULL
import json
import os
import os.path as osp
import io
import base64
from tkinter import W
from PIL import Image
from PIL import ImageOps
from PIL import ExifTags
import re
from labelme import utils




def apply_exif_orientation(image):  
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None
 
    if exif is None:
        return image
 
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in exif.items()
        if k in ExifTags.TAGS
    }
 
    orientation = exif.get('Orientation', None)
 
    if orientation == 1:
        # do nothing
        return image
    elif orientation == 2:
        # left-to-right mirror
        return ImageOps.mirror(image)
    elif orientation == 3:
        # rotate 180
        return image.transpose(Image.ROTATE_180)
    elif orientation == 4:
        # top-to-bottom mirror
        return ImageOps.flip(image)
    elif orientation == 5:
        # top-to-left mirror
        return ImageOps.mirror(image.transpose(Image.ROTATE_270))
    elif orientation == 6:
        # rotate 270
        return image.transpose(Image.ROTATE_270)
    elif orientation == 7:
        # top-to-right mirror
        return ImageOps.mirror(image.transpose(Image.ROTATE_90))
    elif orientation == 8:
        # rotate 90
        return image.transpose(Image.ROTATE_90)
    else:
        return image

def load_image_file(filename, rote=False):  #labelme内自带读取图片函数
    try:
        image_pil = Image.open(filename)
        if rote:
            image_pil = image_pil.transpose(Image.ROTATE_270)
    except IOError:
        #print('Failed opening image file: {}'.format(filename))
        return None
 
# apply orientation to image according to exif
    image_pil = apply_exif_orientation(image_pil)
 
    with io.BytesIO() as f:
        ext = osp.splitext(filename)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            format = 'JPEG'
        else:
            format = 'PNG'
        image_pil.save(f, format=format)
        f.seek(0)
        return f.read()
 
def convert2shape(line,height,width):  # 坐标转换
    line = line.rstrip().split(' ')

    '''
    这里修改类别名称
    '''
    if int(line[0]) == 1:
        label = 'plane'
    if int(line[0]) == 2:
        label = 'ship'
    if int(line[0]) == 3:
        label = 'seating'
    if int(line[0]) == 4:
        label = 'FSJ'
    if int(line[0]) == 5:
        label = 'TT'
    if int(line[0]) == 6:
        label = 'Radar'
    else:
        label = 'Radar'
    cx = float(line[1])
    cy = float(line[2])
    w = float(line[3])
    h = float(line[4])


    x1      = (cx-w/2.0)*width
    y1      = (cy-h/2.0)*height
    x2      = (cx+w/2.0)*width
    y2      = (cy+h/2.0)*height

    points = [[x1,y1],[x2,y2]]
    return points,label


def conver_labelme(txt_floder_path, json_output_path, image_path,img_h,img_w):
    txt_names = os.listdir(txt_floder_path)
    for txt_name in txt_names:
        img_name = txt_name[0:-4] + '.jpg'
        json_name = txt_name[0:-4] + '.json'
        img = load_image_file(osp.join(image_path + img_name))
        label_dict = {"version": "5.0.1", "flags": {}, "shapes": [], "imagePath": '', "imageData": '', "imageHeight": 0, "imageWidth": 0}
        label_dict["imagePath"] = img_name
        label_dict["imageData"] = base64.b64encode(img).decode('utf-8') #此时imageData是unicode格式，需要转成str
        label_dict["imageHeight"] = img_h
        label_dict["imageWidth"] = img_w

        with open(os.path.join(txt_floder_path,txt_name),"r") as file:
            lines = file.readlines()   
            for line in lines:
                points,label =  convert2shape(line,img_h,img_w)
                shape = {"label": label, "points": points, "group_id": None, "shape_type": "rectangle", "flags": {}}
                label_dict["shapes"].append(shape)

        with open(os.path.join(json_output_path) + json_name,"w") as f:
            f.write(json.dumps(label_dict))
        f.close


if __name__ == "__main__":
    img_h = 720
    img_w = 1280
    txt_floder_path = 'yolo_label_test/txt/'    # 存放yolo标签的位置
    image_path = 'yolo_label_test/images/'      # 存放图像的位置
    json_output_path = 'yolo_label_test/json/'  # 保存生成json的位置
    conver_labelme(txt_floder_path, json_output_path, image_path,img_h,img_w)
    print("All label of valid images have been convered successfully!")