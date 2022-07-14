"""
Usage:
Takes all images from a directory and resizes them, making them smaller if above X.
Start: 
Input a directory to work from.
The script walks through all files within the directory.
If the image is above size X, it gets resized and saved over the original.
"""

import os    # Using os.replace(), os.sep(), os.walk(), os.path.join(), os.path.getsize()
from PIL import Image

# grab working directory
startDir = input('Specify FULL PATH to local content directory: ')

# The extensions to search through
fileExtensions = ('.jpg', '.jpeg', '.png')

# walk through all files in directory
for dirPath, dirNames, allFiles in os.walk(startDir):
    for name in allFiles:
        filePath = os.path.join(dirPath, name)
        fileSize = os.path.getsize(filePath)
        # check if file has image extension and large size - above 0.5MB
        if name.endswith(fileExtensions) and fileSize > 524288:
            # resize image
            with Image.open(filePath) as im:
                if fileSize < 786432:
                    # Provide the target width and height of the image
                    (width, height) = (int(im.width * 0.75), int(im.height * 0.75))
                elif fileSize < 1048576:
                    # Provide the target width and height of the image
                    (width, height) = (int(im.width * 0.5), int(im.height * 0.5))
                else:
                    # Provide the target width and height of the image
                    (width, height) = (int(im.width * 0.25), int(im.height * 0.25))
                imResized = im.resize((width, height))
            imResized.save(dirPath + os.sep + "tmp-" + name, "png")
            tmpFilePath = os.path.join(dirPath, "tmp-" + name)
            os.replace(tmpFilePath, filePath)
