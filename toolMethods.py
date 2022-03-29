import glob
from PIL import Image
from sql import SqlProcess
from createPhotomosaic import createPhotomosaic
import cv2
import os
import numpy as np
from sql import SqlProcess

RANGE_VALUE = 30
class toolMethods:
    def createImageGrid(images, dims):
        m, n = dims
        width = max([img.size[0] for img in images])
        height = max([img.size[1] for img in images])
        grid_img = Image.new('RGB', (n * width, m * height))
        for index in range(len(images)):
            # getoffset
            row = int(index / n)
            col = index - n * row
            grid_img.paste(images[index], (col * width, row * height))
        return (grid_img)

    def getMatchValuesDb(avg, db):
            result = db.query_tree(avg)
            return result

    def splitImage(image, size):
            W, H = image.size[0], image.size[1]
            m, n = size
            w, h = int(W / n), int(H / m)
            imgs = []
            for j in range(m):
                for i in range(n):
                    imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
            return (imgs)

    def getAverageRGB(image):
            im = np.array(image)
            w, h, d = im.shape
            return (np.average(im.reshape(w * h, d), axis=0))

    def getBestMatchIndexDb(avg, avgs):
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