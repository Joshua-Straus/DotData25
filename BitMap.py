import math
import matplotlib.pyplot as plt
import numpy as np

#Authors: Caden Udani, Joshua Straus
#Creates a Pixel object that has a RGB value and a toString
class Pixel:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
    def toString(self):
        return self.red , self.green , self.blue

#Author: Joshua Straus
#Houses a name + a pixel object
class Color:
    def __init__(self, name, pixel):
        self.pixel = pixel
        self.name = name

#Authors: Joshua Straus, Caden Udani
#A BitMap file format that can simplify down to a simple collection of colors, has visualization abilities, and can return an average greyscale value
class BitMap:

    #The collection of colors we will use for analysis
    colors = [Color("Maroon", Pixel(128,0,0)), Color("Red",Pixel(230,25,75)), Color("Pink",Pixel(250,190,212)), Color("Brown",Pixel(170,110,40)), Color("Orange", Pixel(245,130,48)), Color("Apricot", Pixel(255,215,180)), Color("Olive",Pixel(128,128,0)), Color("Yellow",Pixel(255,255,25)), Color("Beige", Pixel(255,250,200)), Color("Lime",Pixel(210,245,60)), Color("Green", Pixel(60,180,75)), Color("Mint", Pixel(170,255,195)), Color("Teal", Pixel(0,128,128)), Color("Cyan", Pixel(70,240,240)), Color("Navy", Pixel(0,0,128)), Color("Blue", Pixel(0,130,200)), Color("Purple", Pixel(145,30,180)), Color("Lavender", Pixel(220,190,255)), Color("Magenta", Pixel(240,50,230)), Color("Black", Pixel(0,0,0)), Color("Grey", Pixel(128,128,128)), Color("White", Pixel(255,255,255))]
    
    #Author: Caden Udani
    #Constructor
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.mp =  [[0 for x in range(width)] for y in range(height)]
        self.name = name
    
    #Author: Caden Udani
    def getName(self):
        return self.name
    
    #Author: Caden Udani
    def getWidth(self):
        return self.width
    
    #Author: Caden Udani
    def getHeight(self):
        return self.height
    
    #Author: Caden Udani
    #Sets the a color to a location on the 2d array
    def set(self, color, row, column):
        if(column >= self.width or row >= self.height or column < 0 or row < 0):
            return False
        self.mp[row][column] = color
        return True
    
    #Author: Caden Udani
    #Returns a color from a location
    def get(self, row, column):
        if(column >= self.width or row >= self.height or column < 0 or row < 0):
            pass
        return self.mp[row][column]
    
    #Simple print
    def printMap(self):
        for i in range(self.getHeight()):
            for j in range(self.getWidth()):
                print(self.mp[i][j].toString())

    #Author: Joshua Straus
    #Simplification algorithm to condense all possible RGB values to a simple set
    def simplify(self):

        #List for the number of each simple color appearing in image
        numOfEachColor = [0] * len(BitMap.colors)

        #Iterates through table
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):

                #List for distance values between a single pixel and each simple color in set
                distances = []

                #Iterates through simple colors
                for color in range(len(BitMap.colors)):

                    #Calculates the magnitude difference between the R, G, and B values of the pixel to the simple color
                    redDif = (self.mp[row][col].pixel.red - BitMap.colors[color].pixel.red)
                    greenDif = (self.mp[row][col].pixel.green - BitMap.colors[color].pixel.green)
                    blueDif = (self.mp[row][col].pixel.blue - BitMap.colors[color].pixel.blue)

                    #Calculates Euclidean distance between pixel and simple color
                    distance = math.sqrt( redDif**2 + greenDif**2 + blueDif**2 )
                    distances.append(distance)

                #Sets pixel to closest color in set    
                self.set(BitMap.colors[distances.index(min(distances))], row, col)

                #Increments the number of the closest color used in poster
                numOfEachColor[distances.index(min(distances))] += 1

        #Calculates colors as a percentage        
        for i in range(len(numOfEachColor)):
            numOfEachColor[i] = numOfEachColor[i] / (self.width * self.height)
        
        #Returns percentage values
        return numOfEachColor
    
    #Author: Joshua STraus
    #Returns the total shade of the image from 0 (black) - 255(white)
    def getGreyValue(self):

        #Total amount of light in image
        totalMagnitude = 0

        #Iterates through table
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                totalMagnitude += self.get(row, col).pixel.red + self.get(row, col).pixel.green + self.get(row, col).pixel.blue

        #Returns total amount of light divided by number of color bytes
        return totalMagnitude / (3 * self.width * self.height)

    #Author: ChatGPT (Used only for testing, not the actual project)
    def visualize_pixel_array(self):
        # Determine image dimensions
        height = len(self.mp)
        width = len(self.mp[0]) if height > 0 else 0

        # Create a NumPy array for the image data (height x width x 3 for RGB)
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Populate the NumPy array with the pixel data
        for i in range(height):
            for j in range(width):
                p = self.mp[i][j]
                image[i, j] = [p.pixel.red, p.pixel.green, p.pixel.blue]
        plt.imshow(image)
        plt.axis("off")  # Hide axes
        plt.show()
