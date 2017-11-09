import cv2
import os
from os import listdir
from os.path import isfile, join, splitext


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def crop_center(img, crop_x, crop_y):
    y, x = img.shape[:2]
    start_x = x//2-(crop_x//2)
    start_y = y//2-(crop_y//2)
    return img[start_y:start_y+crop_y,start_x:start_x+crop_x]


image_pixels_width = 64
src_path_root = 'img/'
dest_path_root = 'out/'
if not os.path.exists(dest_path_root):
    os.makedirs(dest_path_root)

sub_dirs = get_immediate_subdirectories(src_path_root)
for directory in sub_dirs:
    src_path = join(src_path_root, directory)
    dest_path = join(dest_path_root, directory)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    onlyfiles = [f for f in listdir(src_path) if isfile(join(src_path, f))]

    for index, file in enumerate(onlyfiles):
        image = cv2.imread(join(src_path, file))
        image_pixels_height = int(image.shape[0] * image_pixels_width / image.shape[1])
        if image_pixels_width >= 32 and image_pixels_height >= 32:
            dim = (image_pixels_width, image_pixels_height)
            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            cropped = crop_center(resized, 32, 32)
            cropped_name = splitext(file)[0] + 'cp' + str(index) + '.jpg'
            cv2.imwrite(join(dest_path, cropped_name), cropped)
