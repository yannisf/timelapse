"""Compiles a timelapse from images"""

import os
import subprocess

ORIG_DIR = 'photos/originals/'
WORK_DIR = 'photos/work/'
ZOOM_OUT = False

FFMPEG = 'avconv'
CONVERT = 'convert'
MOGRIFY = 'mogrify'

x_original = 4000
y_original = 2600

x_final = 1920
y_final = 1080

num_of_images = len(os.listdir(ORIG_DIR))

x_coefficient = (x_original - x_final) / (num_of_images - 1)
y_coefficient = (y_original - y_final) / (num_of_images - 1)

def convert_originals():
    """Converts originals to the initial resolutions, writing them to the work dir in the same time"""
    for i, f in enumerate(sorted(os.listdir(ORIG_DIR), key=extract_num_part)):
        command = '{} -gravity center -crop {}x{}+0+0 {} {}' \
            .format(CONVERT, x_original, y_original, ORIG_DIR + f, WORK_DIR + str(i).zfill(5) + '.JPG')
        print(command)
        subprocess.call(command, shell=True)

def extract_num_part(filename):
    """Extracts the numeric part of a photo that has the name format XXX_NUM.JPG"""
    underscrore_index = filename.index('_')
    dot_index = filename.index('.')
    return filename[underscrore_index+1:dot_index]

def x_size(idx):
    return int(x_original - x_coefficient * idx)

def y_size(idx):
    return int(y_original - y_coefficient * idx)

def zoom_crop():
    """Crops images from the work dir to create a zoom effect"""
    for i, f in enumerate(sorted(os.listdir(WORK_DIR), reverse=ZOOM_OUT)):
        command = '{} -gravity center -crop {}x{}+0+0 {}'.format(MOGRIFY, x_size(i), y_size(i), WORK_DIR + f)
        print(command)
        subprocess.call(command, shell=True)

def final_resize():
    for f in os.listdir(WORK_DIR):
        command = '{} -resize {}x{}! {}'.format(MOGRIFY, x_final, y_final, WORK_DIR + f)
        print(command)
        subprocess.call(command, shell=True)

def create_video():
    command = "{} -r 10 -framerate 30 -i %05d.JPG out.mkv".format(FFMPEG)
    print(command)
    subprocess.call(command, shell=True)

def mux_audio():
    command = '{} -i ../../audio/audio.mp3 -i out.mkv -c copy video.mkv'.format(FFMPEG)
    print(command)
    subprocess.call(command, shell=True)

convert_originals()
zoom_crop()
final_resize()
os.chdir(WORK_DIR)
create_video()
mux_audio()
