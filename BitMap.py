import math
import matplotlib.pyplot as plt
import numpy as np

class Pixel:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
    def toString(self):
        return self.red , self.green , self.blue

class Color:
    def __init__(self, name, pixel):
        self.pixel = pixel
        self.name = name

class BitMap:
    colors = [Color("Maroon", Pixel(128,0,0)), Color("Red",Pixel(230,25,75)), Color("Pink",Pixel(250,190,212)), Color("Brown",Pixel(170,110,40)), Color("Orange", Pixel(245,130,48)), Color("Apricot", Pixel(255,215,180)), Color("Olive",Pixel(128,128,0)), Color("Yellow",Pixel(255,255,25)), Color("Beige", Pixel(255,250,200)), Color("Lime",Pixel(210,245,60)), Color("Green", Pixel(60,180,75)), Color("Mint", Pixel(170,255,195)), Color("Teal", Pixel(0,128,128)), Color("Cyan", Pixel(70,240,240)), Color("Navy", Pixel(0,0,128)), Color("Blue", Pixel(0,130,200)), Color("Purple", Pixel(145,30,180)), Color("Lavender", Pixel(220,190,255)), Color("Magenta", Pixel(240,50,230)), Color("Black", Pixel(0,0,0)), Color("Grey", Pixel(128,128,128)), Color("White", Pixel(255,255,255))]
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.mp =  [[0 for x in range(width)] for y in range(height)]
        self.name = name
    
    def getName(self):
        return self.name
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def set(self, pixel, row, column):
        if(column >= self.width or row >= self.height or column < 0 or row < 0):
            return False
        self.mp[row][column] = pixel
        return True
    
    def get(self, row, column):
        if(column >= self.width or row >= self.height or column < 0 or row < 0):
            pass
        return self.mp[row][column]
    
    def printMap(self):
        for i in range(self.getHeight()):
            for j in range(self.getWidth()):
                print(self.mp[i][j].toString())

    def simplify(self):
        numOfEachColor = [0] * len(BitMap.colors)
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                distances = []
                for color in range(len(BitMap.colors)):
                    redDif = (self.mp[row][col].red - BitMap.colors[color].pixel.red)
                    greenDif = (self.mp[row][col].green - BitMap.colors[color].pixel.green)
                    blueDif = (self.mp[row][col].blue - BitMap.colors[color].pixel.blue)
                    distance = math.sqrt(pow(redDif, 2) + pow(greenDif, 2) + pow(blueDif, 2))
                    distances.append(distance)
                self.set(BitMap.colors[distances.index(min(distances))], row, col)
                numOfEachColor[distances.index(min(distances))] += 1
        for i in range(len(numOfEachColor)):
            numOfEachColor[i] = numOfEachColor[i] / (self.width * self.height)
        return numOfEachColor
    


    def visualize_pixel_array(self):
        # Determine image dimensions
        height = len(self.mp)
        width = len(self.mp[0]) if height > 0 else 0

        # Create a NumPy array for the image data (height x width x 3 for RGB)
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Populate the NumPy array with the pixel data
        for i in range(height):
            for j in range(width):
                p = self.mp[i][j].pixel
                image[i, j] = [p.red, p.green, p.blue]
        plt.imshow(image)
        plt.axis("off")  # Hide axes
        plt.show()
