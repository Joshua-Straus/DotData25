from PIL import Image
import requests
from io import BytesIO
from BitMap import BitMap, Pixel

"""
url = "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg"
response = requests.get(url)
if (response.status_code == 200):
    with open("downloaded_image.jpg", "wb") as file:
        file.write(response.content)
img = Image.open("downloaded_image.jpg")
img.save("output.ppm")
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

print(ppmToBitMap("test.ppm").printMap())


"""
def parse(ppmFile):
    file = open(ppmFile)
    for line in file:
        if line[0] != '#':
            for token in line.split():
                yield token

def ppmToBitMap(ppmFile):
    token = parse(ppmFile)
    nextToken = lambda : next(token)
    assert 'P6' == nextToken(), 'Not a PPM6 File'
    width, height, maxBitValue = (int(next()) for i in range(3))
    bitmap = BitMap(width, height, "Name")
    for h in range(height-1, -1, -1):
        for w in range(0, width):
            bitmap.set(w, h, Pixel( *(int(next()) for i in range(3))))

    return bitmap
"""

#print(ppmToBitMap("output.ppm"))

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
                    imageBytes = BytesIO(response.content)
                    img = Image.open(imageBytes)
                    jpgs.append(img)
                    counter += 1
                    print(counter)
except FileNotFoundError:
    print("File not found")
except csv.Error as error:
    print(f"CSV Error: {error}")

print("Done")

#JPG file
#img = Image.open("input.jpg")

#to PPM
#img.save("output.ppm")

"""