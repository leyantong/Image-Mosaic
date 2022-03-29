# Image-Mosaic
An Image Mosaic tool which can convert image/video into mosaic image in artistic effect using customised library sources.

## Installation

```bash
git clone https://github.com/leyantong/Image-Mosaic.git
```

## Usage

```python
# setup database for the image matching preprocessing using R* tree 
python3 libraryPreprocessing.py --images_directory [library path]
# setup json file for the image matching preprocessing using brute force
python3 preprocessing.py --path [library path]
# convert image/video into mosaic image in artistic effect using customised library sources.
python3 process.py --type [image/video] --target [target filename] --images [library path] --grid [number of grid] --process [on/off] --output [output filename]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
