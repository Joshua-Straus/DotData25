class BitMap:

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
    


class Pixel:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
    def toString(self):
        return self.red , self.green , self.blue