# TODO Add more documentation over these functions

def powerCalculator(w: str='', v: str='', a: str=''):

    result = 0.0
    solvedFor = ''
    
    if w == '':
        result = float(v) * float(a)
        solvedFor = 'w'
    elif v == '':
        result = float(w) / float(a)
        solvedFor = 'v'
    elif a == '':
        result = float(w) / float(v)
        solvedFor = 'a'

    return result, solvedFor

def addressCalculator(addresses: int, numberFixtures: int, startingAddress=1):
    
    result: list = [f"1: {startingAddress}"]

    for i in range(1, numberFixtures):

        nextFixture = f"{i + 1}: {i * addresses + startingAddress}"
        result.append(nextFixture)

    return result


import lib.requests
import shutil

def downloadImage(url: str):

    # Define file name
    fileName = url.split("/")[-1]

    # Request stream
    r = lib.requests.get(url, stream=True)

    # Check if successful, handle if not
    if r.status_code == 200:
        r.raw.decode_content = True

        # Write to local file
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return True
    
    else:

        return False


import os
import io
from PIL import Image

def imageToMemory(fileName: str, sizeX: int, sizeY: int, bio):
    if os.path.exists(fileName):
                    image = Image.open(fileName)
                    image.thumbnail((sizeX, sizeY))
                    image.save(bio, format="PNG")