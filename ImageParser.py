from PIL import Image
import requests
from io import BytesIO
from BitMap import BitMap, Pixel
import csv
import pandas as pd
"""
def ppmToBitMap(ppmFile):
    with open(ppmFile, 'rb') as file:
        header = file.readline().decode('ascii').strip()
        if (header != 'P6'):
            pass
        imageDimensions = file.readline().decode('ascii').strip().split()
        width = int(imageDimensions[0])
        height = int(imageDimensions[1])
        maxColor = int(file.readline().decode('ascii').strip())
        bm = BitMap(width, height, "Test")
        pixels = bytearray(file.read())
        startIndex = 0
        for row in range(height):
            for col in range(width):
                currentPixel = pixels[startIndex:startIndex + 3]
                if len(currentPixel) < 3:
                    print("Not enough pixel data")
                    pass
                r, g, b = currentPixel[0], currentPixel[1], currentPixel[2]
                p = Pixel(r,g,b)
                bm.set(p, row, col)
                startIndex += 3
    return bm
"""
def ppmToBitMap(ppmFile):
    file = ppmFile
    header = file.readline().decode('ascii').strip()
    if (header != 'P6'):
        pass
    imageDimensions = file.readline().decode('ascii').strip().split()
    width = int(imageDimensions[0])
    height = int(imageDimensions[1])
    #maxColor = int(file.readline().decode('ascii').strip())
    bm = BitMap(width, height, "Test")
    pixels = bytearray(file.read())
    startIndex = 0
    for row in range(height):
        for col in range(width):
            currentPixel = pixels[startIndex:startIndex + 3]
            if len(currentPixel) < 3:
                print("Not enough pixel data")
                return bm
            r, g, b = currentPixel[0], currentPixel[1], currentPixel[2]
            p = Pixel(r,g,b)
            bm.set(p, row, col)
            startIndex += 3
    return bm

"""
jpgs = []
counter = 0
try:
    with open('imdb_top_1000.csv', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if (".jpg" in row[0]):
                response = requests.get(row[0])
                if response.status_code  == 200:
                    image = Image.open(BytesIO(response.content))
                    ppmBuffer = BytesIO()
                    image.save(ppmBuffer, format='PPM')
                    ppmBuffer.seek(0)
                    bm = ppmToBitMap(ppmBuffer)
                    bm.simplify()
"""
try:
    counter = -1
    df = pd.read_csv("imdb_top_1000.csv", encoding="utf-8")
    for i in range(len(BitMap.colors)):
        df[BitMap.colors[i].name] = None
    for value in df["Poster_Link"]:
        counter += 1
        if (".jpg" in value):
            response = requests.get(value)
            if response.status_code == 200:
                byte_stream = BytesIO(response.content)
                if (byte_stream.read(2) != b'\xff\xd8'):
                    print("Bad")
                    continue
                if (value == "https://m.media-amazon.com/images/M/MV5BOGQzODdlMDktNzU4ZC00N2M3LWFkYTAtYTM1NTE0ZWI5YTg4XkEyXkFqcGdeQXVyMTA1NTM1NDI2._V1_UX67_CR0,0,67,98_AL_.jpg" or value == "https://m.media-amazon.com/images/M/MV5BMTYxMDk1NTA5NF5BMl5BanBnXkFtZTcwNDkzNzA2NA@@._V1_UX67_CR0,0,67,98_AL_.jpg"):
                    continue
                image = Image.open(byte_stream)
                ppmBuffer = BytesIO()
                image.save(ppmBuffer, format='PPM')
                ppmBuffer.seek(0)
                bm = ppmToBitMap(ppmBuffer)
                valueList = bm.simplify()
                for i in range (len(BitMap.colors)):
                    df.loc[counter, BitMap.colors[i].name] = valueList[i]
                print(counter , value)
    df.to_csv("newCSV.csv")
except FileNotFoundError:
    print("File not found")
except csv.Error as error:
    print(f"CSV Error: {error}")

print("Done")