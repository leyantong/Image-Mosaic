from ast import arg
import json
from PIL import Image
import argparse
from sql import SqlProcess
from createPhotomosaic import createPhotomosaic
import cv2
import os
from toolMethods import toolMethods
import timeit

def videoProcessing(target):
    dirname = 'test'
    os.mkdir(dirname)
    cap= cv2.VideoCapture(target)
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(os.path.join(dirname, str(i)+'.jpg'), frame)
        i+=1
    cap.release()
    cv2.destroyAllWindows()
    return dirname

def load_images_from_folder(folder):
    images = []
    count = 0
    trigger = True
    while trigger:
        try:
            img = Image.open(os.path.join(folder,str(count)+'.jpg'))
            if img is not None:
                images.append(img)
            count+=1
        except:
            trigger = False
    return images

def processVideo(path):
    img_array = []
    flag = True
    count = 0
    size = None
    while flag:
        try:
            img = cv2.imread(path+'/'+str(count)+'.jpg')
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

def create_images_using_db(target_image, grid_size, dims, db, path):
    target_images = toolMethods.splitImage(target_image, grid_size)
    indexes = []
    images = []
    print("number of tiles:"+ str(len(target_images)))
    for img in target_images:
        avg = toolMethods.getAverageRGB(img)
        result = toolMethods.getMatchValuesDb(avg, db)
        if result:
                indexes.append(result[0])
    for index in indexes:
        filePath = os.path.abspath(os.path.join(str(args.images), str(index)+'.JPG'))
        try:
            fp = open(filePath, "rb")
            im = Image.open(fp)
            im.thumbnail(dims)
            images.append(im)
            im.load()
            fp.close()
        except:
            print("Invalid image: %s" % (filePath,))
    print("starting to create image...")
    mosaic_image = toolMethods.createImageGrid(images, grid_size)
    mosaic_image.save(path+'.JPG', 'jpeg')


# Sources and settings
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    parser.add_argument('--type', dest='type', required=True, help="video or image")
    parser.add_argument('--target', dest='target', required=True, help="Image to create mosaic from")
    parser.add_argument('--images', dest='images', required=True, help="Diectory of images")
    parser.add_argument('--grid', nargs=2, dest='grid', required=True, help="Size of photo mosaic")
    parser.add_argument('--output', dest='output', required=False)
    parser.add_argument('--process', dest='process', required=True)
    args = parser.parse_args()
    if args.type == 'video':
        dirname = videoProcessing(args.target)
        images = load_images_from_folder(dirname)
        grid_size = (int(args.grid[1]), int(args.grid[0]))
        # size of target image
        target_size = (int(images[0].size[1]), int(images[0].size[0]))
        dims = (int(target_size[0] / grid_size[1]),
                        int(target_size[1] / grid_size[0]))
        # processs library images
        db = SqlProcess("db")
        path = "/Users/leyton01/Desktop/third-year-project/project/output"
        os.mkdir('output')
        count = 0
        for frame in images:
            path1 = f"{path}/{str(count)}"
            create_images_using_db(frame, grid_size, dims, db, path1)
            count += 1
        processVideo(path)

    if args.type == 'image':
        target_image = Image.open(args.target)
        # size of grid
        grid_size = (int(args.grid[1]), int(args.grid[0]))
        # size of target image
        target_size = (int(target_image.size[1]), int(target_image.size[0]))
        dims = (int(target_size[0] / grid_size[1]),
                        int(target_size[1] / grid_size[0]))
        if args.process == 'on':
            start = timeit.default_timer()
            db = SqlProcess("db")
            path = str(args.output)
            create_images_using_db(target_image, grid_size, dims, db, path)
            

        if args.process == 'off':
            start = timeit.default_timer()
            # processs library images
            filename = str(args.images)
            # output
            output_filename = 'mosaic1.jpeg'
            if args.output:
                output_filename = args.output
            with open(filename) as json_file:
                data = json.load(json_file)
            createPhotomosaic = createPhotomosaic(target_image, data, grid_size)
            # write out mosaic
            mosaic_image = createPhotomosaic.createPhoto(target_image, dims)
            mosaic_image.save(output_filename, 'jpeg')

            print("saved output to %s" % (output_filename,))
            print('done.')
        stop = timeit.default_timer()
        print('Time: ', stop - start)  

