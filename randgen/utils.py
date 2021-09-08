import os

def isValidFile(filename, extension):
    _, fileExtension = os.path.splitext(filename)
    return fileExtension == extension