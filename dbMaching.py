# pre process thwe images, crop the images and store them into a tree
import glob
import imp
from PIL import Image
from scipy import spatial
import numpy as np
import sys, os, random
import argparse
import sqlite3
from sqlite3 import Error
from sql import SqlProcess
from preProcessing import RANGE_VALUE
import cv2

class dbMatching:
    def __init__(self):
        self.images_list = None
    
    def splitImage(self, image, size):
        W, H = image.size[0], image.size[1]
        m, n = size
        w, h = int(W / n), int(H / m)
        imgs = []
        for j in range(m):
            for i in range(n):
                imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
        return (imgs)
    
    def getAverageRGB(self, image):
        im = np.array(image)
        w, h, d = im.shape
        return (np.average(im.reshape(w * h, d), axis=0))

    def getBestMatchIndexDb(self, input_avg, avgs):
        avg = input_avg
        min_index = 0
        min_dist = float("inf")
        for val in avgs:
            print('111'+ type(val))
            print(val)
            r, g, b = val[1] + RANGE_VALUE, val[3] + RANGE_VALUE, val[5] + RANGE_VALUE
            dist = ((r - avg[0]) * (r - avg[0]) +
                    (g - avg[1]) * (g - avg[1]) +
                    (b - avg[2]) * (b - avg[2]))
            if dist < min_dist:
                min_dist = dist
                min_index = val[0]
        return (min_index)
    
    def getMatchValuesDb(self, avg):
        db = SqlProcess('db')
        result = db.query_tree(avg)
        return result

    def createPhoto(self, target_image, grid_size):
        # split image into small size of mosaic
        target_images = self.splitImage(target_image, grid_size)
        output_images = []
        avgs = []
        # query the tree with rgb value to find a set of similar rgb values
        for img in target_images:
            avg = self.getAverageRGB(img)
            result = self.getMatchValuesDb(avg)
            if result:
                match_index = self.getBestMatchIndexDb(avg, result)
            else:
                match_index = self.getBestMatchIndex(avg, avgs)
            output_images.append(self.library_images[match_index])

        mosaic_image = self.createImageGrid(output_images, self.grid_size)
        return (mosaic_image)
    
    

    


