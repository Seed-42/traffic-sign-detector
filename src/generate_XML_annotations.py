from collections import defaultdict
import os
import csv
from PIL import Image
from sklearn.model_selection import train_test_split
import pandas as pd

from xml.etree.ElementTree import parse, Element, SubElement, ElementTree
import xml.etree.ElementTree as ET

# Create folder to write annotations.
folder = "pascal_xml_annotation"
train_folder = folder + "/train"
test_folder = folder + "/test"
if not os.path.exists(folder):
    os.mkdir(folder)
if not os.path.exists(train_folder):
    os.mkdir(train_folder)
if not os.path.exists(test_folder):
    os.mkdir(test_folder)


def write_xml(folder, filename, bbox_list):
    root = Element('annotation')
    SubElement(root, 'folder').text = folder
    SubElement(root, 'filename').text = filename
    SubElement(root, 'path').text = filename
    source = SubElement(root, 'source')
    SubElement(source, 'database').text = 'Unknown'

    # Details from first entry
    e_filename, e_width, e_height, e_class_name, e_xmin, e_ymin, e_xmax, e_ymax = bbox_list[0]

    size = SubElement(root, 'size')
    SubElement(size, 'width').text = e_width
    SubElement(size, 'height').text = e_height
    SubElement(size, 'depth').text = '3'

    SubElement(root, 'segmented').text = '0'

    for entry in bbox_list:
        e_filename, e_width, e_height, e_class_name, e_xmin, e_ymin, e_xmax, e_ymax = entry

        obj = SubElement(root, 'object')
        SubElement(obj, 'name').text = e_class_name
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'

        bbox = SubElement(obj, 'bndbox')
        SubElement(bbox, 'xmin').text = e_xmin
        SubElement(bbox, 'ymin').text = e_ymin
        SubElement(bbox, 'xmax').text = e_xmax
        SubElement(bbox, 'ymax').text = e_ymax

    # indent(root)
    tree = ElementTree(root)

    xml_filename = os.path.join(folder, os.path.splitext(filename)[0] + '.xml')
    tree.write(xml_filename)


# MAIN ############

df = pd.read_csv("images/annotations.csv")
y = df["class"]
X = df.drop(columns=['class'])

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

X_train["class"] = y_train
train_data = X_train
print(train_data.sample(10))
print(train_data.shape)

X_test["class"] = y_test
test_data = X_test
print(test_data.sample(10))
print(test_data.shape)

train_entries_by_filename = defaultdict(list)
test_entries_by_filename = defaultdict(list)

# train data
for index, row in train_data.iterrows():
    filename, xmin, ymin, xmax, ymax, op_class = row

    img = Image.open(f"images/{filename}")
    img_width = int(img.size[0])
    img_height = int(img.size[1])

    roq_mod = [filename, str(img_width), str(img_height), op_class, str(xmin), str(ymin), str(xmax), str(ymax)]

    # Save image
    img.save(f"{train_folder}/{filename}", format="png")
    print(f"Image saved to {train_folder}/{filename}")

    train_entries_by_filename[filename].append(roq_mod)

for filename, entries in train_entries_by_filename.items():
    print(filename, len(entries))
    write_xml(train_folder, filename, entries)

# test data
for index, row in test_data.iterrows():
    filename, xmin, ymin, xmax, ymax, op_class = row

    img = Image.open(f"images/{filename}")
    img_width = int(img.size[0])
    img_height = int(img.size[1])

    # Save image
    img.save(f"{test_folder}/{filename}", format="png")
    print(f"Image saved to {test_folder}/{filename}")

    roq_mod = [filename, str(img_width), str(img_height), op_class, str(xmin), str(ymin), str(xmax), str(ymax)]

    test_entries_by_filename[filename].append(roq_mod)

for filename, entries in test_entries_by_filename.items():
    print(filename, len(entries))
    write_xml(test_folder, filename, entries)
