import xml.etree.ElementTree as ET
import pickle
import os
import sys
from glob import glob

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_fn):
    if not os.path.isfile(xml_fn):
        print("the file: {} cannot be found".format(xml_fn))
        return
    else:
        print("Opening XML file: {}".format(xml_fn))
        in_file = open(xml_fn)

        txt_fn=xml_fn.replace(".xml",".txt")
        out_file = open(txt_fn, 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        #size = root.find('size')
        #w = int(size.find('width').text)
        #h = int(size.find('height').text)

        #for obj in root.iter('object'):
        #    difficult = obj.find('difficult').text
        #    cls = obj.find('name').text
        #    if cls not in classes or int(difficult) == 1:
        #        continue
        #    cls_id = classes.index(cls)
        #    xmlbox = obj.find('bndbox')
        #    b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        #    bb = convert((w,h), b)
        #    #out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        #    out_file.write(f"{cls_id} {bb[0]:0.6f} {bb[1]:0.6f} {bb[2]:0.6f} {bb[3]:0.6f}\n")
        #    #print(f"{txt_fn} created")
        in_file.close()
        out_file.close()


if len(sys.argv) != 4:
    print("wrong arguments")
    sys.exit(1)
else:
    image_dir = sys.argv[1]
    class_list = sys.argv[2]
    file_list = sys.argv[3]

# image_dir must exit as a directory
if not os.path.isdir(image_dir):
    print("Image_dir: {} cannot be found or is not a directory".format(image_dir))
    sys.exit(1)

# class names must exist as a file
if not os.path.isfile((class_list)):
    print("class_list: {} cannot be found or is not a file".format(class_list))
    sys.exit(1)


# Get the class names from class_list
with open(class_list, "r") as f:
    classes = f.read().split("\n")

classnames = [c for c in classes]
print(classnames, len(classnames))

list_file = open(file_list, "w")

for i, xml_fn in enumerate(glob(image_dir+"/*.xml")):
    image = xml_fn.replace("xml", "jpg")
    list_file.write(image + "\n")
    convert_annotation(xml_fn)
    print("{} converted and added to file list".format(image))
    #if (i+1)%100==0:
    #   print(i+1)
list_file.close()


print("You survived")