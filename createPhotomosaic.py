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
import cv2
RANGE_VALUE = 30
class createPhotomosaic:
    def __init__(self, target_image, images_data, grid_size):
        self.target_image = target_image
        self.images_data = images_data
        self.grid_size = grid_size

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
    
    def getBestMatchIndex(self, input_avg, avgs):
        avg = input_avg
        index = 0
        min_index = 0
        min_dist = float("inf")
        for val in avgs:
            dist = ((val[0] - avg[0]) * (val[0] - avg[0]) +
                    (val[1] - avg[1]) * (val[1] - avg[1]) +
                    (val[2] - avg[2]) * (val[2] - avg[2]))
            if dist < min_dist:
                min_dist = dist
                min_index = index
            index += 1
        return (min_index)
    
    def getBestMatchIndexDb(self, avg, avgs):
        min_index = 0
        min_dist = float("inf")
        print(len(avgs))
        if len(avgs) == 1:
            return avgs[0][0]
        for val in avgs:
            r, g, b = val[1] + RANGE_VALUE, val[3] + RANGE_VALUE, val[5] + RANGE_VALUE
            dist = ((r - avg[0]) * (r - avg[0]) +
                    (g - avg[1]) * (g - avg[1]) +
                    (b - avg[2]) * (b - avg[2]))
            if dist < min_dist:
                min_dist = dist
                min_index = val[0]
        return (min_index)

    def createImageGrid(self, images, dims):
        m, n = dims
        width = max([img.size[0] for img in images])
        height = max([img.size[1] for img in images])
        grid_img = Image.new('RGB', (n * width,  m * height))
        for index in range(len(images)):
            # getoffset
            row = int(index / n)
            col = index - n * row
            grid_img.paste(images[index], (col * width, row * height))
        return (grid_img)
    
    def process(self, path):
        img_array = []
        flag = True
        count = 0
        while flag:
            try:
                img = cv2.imread(path+str(count)+'.jpg')
                height, width, layer = img.shape
                size = (width,height)
                img_array.append(img)
                count += 1
            except:
                flag = False
                
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        out = cv2.VideoWriter('project.avi',fourcc, 30, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()

    def createPhoto(self, target_image, dims):
        # split image into small size of mosaic
        target_images = self.splitImage(target_image, self.grid_size)
        output_images = []
        avgs = []
        # query the tree with rgb value to find a set of similar rgb values
        for value in self.images_data.values():
            try:
                avgs.append(value["avg_value"])
            except ValueError:
                continue

        for img in target_images:
            avg = self.getAverageRGB(img)
            match_index = self.getBestMatchIndex(avg, avgs)
            path = self.images_data[str(match_index)]["path"]
            try:
                    fp = open(path, "rb")
                    im = Image.open(fp)
                    im.thumbnail(dims)
                    output_images.append(im)
                    im.load()
                    fp.close()
            except:
                    print("Invalid image: %s" % (path,))

        mosaic_image = self.createImageGrid(output_images, self.grid_size)
        return (mosaic_image)

    def createVideo(self, target_images):
        os.mkdir('output')
        count = 0
        path = "/Users/leyton01/Desktop/third-year-project/project/output"
        for img in target_images:
            mosaic_image = self.createPhoto(img)
            mosaic_image.save(f"{path}/{str(count)}.jpg")
            count += 1

        path1 = "/Users/leyton01/Desktop/third-year-project/project/output/"
        self.process(path1)

