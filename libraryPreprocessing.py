# pre process thwe images, crop the images and store them into a tree
import glob
from multiprocessing.dummy.connection import Connection
from PIL import Image
from scipy import spatial
import numpy as np
import sys, os, random
import argparse
import sqlite3
from sqlite3 import Error
from sql import SqlProcess
RANGE_VALUE = 30
CREATE_R_TREE = '''
CREATE VIRTUAL TABLE library_data USING rtree(
   id,              -- Integer primary key
   Rmin, Rmax,      -- R
   Gmin, Gmax,       -- G
   Bmin, Bmax        -- B
);
'''

parser = argparse.ArgumentParser()
parser.add_argument('--images_directory', dest='images_directory', required=True, help="images_directory")
args = parser.parse_args()

def getAverageRGB(image):
        im = np.array(image)
        w, h, d = im.shape
        return (np.average(im.reshape(w * h, d), axis=0))

db = SqlProcess("db")
db.execute_query(CREATE_R_TREE)

print('reading library folder...')
files = os.listdir(args.images_directory)
index = 0
for file in files:
    filePath = os.path.abspath(os.path.join(args.images_directory, file))
    try:
        fp = open(filePath, "rb")
        im = Image.open(fp)
        rgb = getAverageRGB(im)
        db.insert_data((index, rgb[0]-RANGE_VALUE, rgb[0]+RANGE_VALUE, rgb[1]-RANGE_VALUE, rgb[1]+RANGE_VALUE, rgb[2]-RANGE_VALUE, rgb[2]+RANGE_VALUE))
        fp.close()
        os.rename(str(filePath), '/Users/leyton01/Desktop/Image-Mosaic/' + str(args.images_directory) + str(index) + ".JPG") 
        index += 1
    except:
        print("Invalid image: %s" % (filePath,))



