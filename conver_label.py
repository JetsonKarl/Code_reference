from asyncio.windows_events import NULL
import json
import os
import os.path as osp
import io
import base64
from PIL import Image
from PIL import ImageOps
from PIL import ExifTags
import re



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
 



def conver_labelme(json_floder_path, output_path, image_path):

    json_names = os.listdir(json_floder_path)
    with open(os.path.join(output_path) + 'label.txt',"w+", encoding = "utf-8") as f_label:
        labels = f_label.read()
        labels = dict(labels)
        i = 0
        for label_key in labels.keys():
            i += 1
        for json_name in json_names:
            json_path = os.path.join(json_floder_path, json_name)
            data = json.load(open(json_path, 'r', encoding='utf-8'))
            label_dict = {"version": "4.6.0", "flags": {}, "shapes": [], "imagePath": '', "imageData": '', "imageHeight": 0, "imageWidth": 0}
            label_dict["imagePath"] = json_name[0:-5] + '.jpg'
            
            #向label的shape键里添加标注物
            for feature in data["markResult"]["features"]:
                label_re = re.sub("[A-Za-z0-9\,\。'_']", "", feature["title"])
                
                if label_re in labels.keys():
                    label = "{}".format(labels[label_re])       #将title所对应的数字序号存入label里
                else:
                    label = "{}".format(i)
                    labels[label_re] = i
                    i += 1
                points = []
                for point in feature["geometry"]["coordinates"][0]: #将每个点添加到points里
                    points.append(point)
                shape = {"label": label, "points": points, "group_id": None, "shape_type": "polygon", "flags": {}}
                label_dict["shapes"].append(shape)
                
            #判断图片是否需要旋转
            if data["info"]["width"] < data["info"]["height"]:
                label_dict["imageHeight"] = data["info"]["width"]
                label_dict["imageWidth"] = data["info"]["height"]
                imageData = load_image_file(osp.join(image_path, json_name[0:-5] + '.jpg'), rote=True)
            else:
                label_dict["imageHeight"] = data["info"]["height"]
                label_dict["imageWidth"] = data["info"]["width"]
                imageData = load_image_file(osp.join(image_path, json_name[0:-5] + '.jpg'))
            #写入图片数据
            if imageData == None:
                pass
            else:
                imageData=base64.b64encode(imageData).decode('utf-8') #此时imageData是unicode格式，需要转成str
                label_dict["imageData"] = imageData
                with open(os.path.join(output_path) + json_name,"w") as f:
                    f.write(json.dumps(label_dict))
                f.close
            
        f_label.write("{}".format(labels))        
    f_label.close()    

            
    
        


if __name__ == "__main__":

    json_floder_path = './json'
    output_path = './labelme/'
    image_path = './images'
    conver_labelme(json_floder_path, output_path, image_path)
    print("All label of valid images have been convered successfully!")