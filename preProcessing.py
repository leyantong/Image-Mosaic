# pre process thwe images, crop the images and store them into a tree
import glob
from multiprocessing.dummy.connection import Connection
from PIL import Image
from scipy import spatial
import numpy as np
import sys, os
from PIL import Image
import json
import argparse
def getAverageRGB(image):
        im = np.array(image)
        w, h, d = im.shape
        return (np.average(im.reshape(w * h, d), axis=0))

def getImagesData(images_directory):
        print('reading library folder...')
        files = os.listdir(images_directory)
        data_dict = {}
        index = 0
        for file in files:
            filePath = os.path.abspath(os.path.join(images_directory, file))
            try:
                fp = open(filePath, "rb")
                im = Image.open(fp)
                avg = getAverageRGB(im)
                avg = (avg[0], avg[1], avg[2])
                data_dict[index] = {}
                data_dict[index]['avg_value'] = avg
                data_dict[index]['path'] = filePath
                im.load()
                fp.close()
                index += 1
            except:
                print("Invalid image: %s" % (filePath,))
        json_object = json.dumps(data_dict, indent = 2)
        # Writing to sample.json
        filename = "data.json"
        with open(filename, "w") as outfile:
            outfile.write(json_object)
        return filename

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(description='generate json file')
        parser.add_argument('--path', dest='path', required=True, help="path of library")
        args = parser.parse_args()
        getImagesData(args.path)


