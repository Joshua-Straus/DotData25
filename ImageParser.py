from PIL import Image
import requests
from io import BytesIO
from BitMap import BitMap, Pixel, Color
import csv
import pandas as pd

#
#   Author: Joshua Straus
#
#   This File uses a CSV file of the IMDB top 1000 movies, parses the file, converts each JPEG of the movie posters to a PPM file,
#   converts the PPM file to a simple BitMap, then creates a new CSV file with the color information and shade information of 
#   each movie's poster
#

#Converts a given P6 PPM file to a BitMap
def ppmToBitMap(ppmFile):
    
    file = ppmFile

    #Ensures file is a P6 PPM
    header = file.readline().decode('ascii').strip()
    if (header != 'P6'):
        pass

    #Parses image dimensions
    imageDimensions = file.readline().decode('ascii').strip().split()
    width = int(imageDimensions[0])
    height = int(imageDimensions[1])
    #max_color
    max_color = int(file.readline().decode('ascii').strip())
    #Creates a new bitmap of a certain dimension
    bm = BitMap(width, height, "Test")

    #Gets the String of Bytes from the PPM
    pixels = bytearray(file.read())

    #Loops through a table of the given dimensions
    startIndex = 0
    for row in range(height):
        for col in range(width):

            #Each 3 bytes constitutes one pixel
            currentPixel = pixels[startIndex:startIndex + 3]

            #Ensures correct formatting
            if len(currentPixel) < 3:
                print("Not enough pixel data")
                return bm
            
            #Sets the BitMap pixel at (row, col) to the correct color
            r, g, b = currentPixel[0], currentPixel[1], currentPixel[2]
            p = Pixel(r,g,b)
            bm.set(Color("initial",p), row, col)

            #Increases by 3 for each 3-byte pixel
            startIndex += 3

    return bm


#Parses the CSV File and creates a new CSV with the color values and shade information
def main():
    
    try:

        #Counter of row, starting at -1 (will be 0 once looping starts)
        counter = -1

        #Creates the data frame
        df = pd.read_csv("imdb_top_1000.csv", encoding="utf-8")

        #Creates new headers in data frame for the selected color values
        for i in range(len(BitMap.colors)):
            df[BitMap.colors[i].name] = None

        #Creates new header for average shade
        df['Shade'] = None

        #Iterates through poster links
        for value in df["Poster_Link"]:
            
            #Counter used to keep track of row number
            counter += 1

            #Ensures we are accessing a file with a JPEG extension
            if (".jpg" in value):

                #Gets info from the URL
                response = requests.get(value)

                #Ensures webpage for URL is up and accessible
                if response.status_code == 200:

                    #Gets content of the webpage
                    byte_stream = BytesIO(response.content)

                    #Ensures this content is encoded as a proper JPEG
                    if (byte_stream.read(2) != b'\xff\xd8'):
                        print("Bad")
                        continue

                    #Bypasses the two faulty links in data set that 
                    if (value == "https://m.media-amazon.com/images/M/MV5BOGQzODdlMDktNzU4ZC00N2M3LWFkYTAtYTM1NTE0ZWI5YTg4XkEyXkFqcGdeQXVyMTA1NTM1NDI2._V1_UX67_CR0,0,67,98_AL_.jpg" or value == "https://m.media-amazon.com/images/M/MV5BMTYxMDk1NTA5NF5BMl5BanBnXkFtZTcwNDkzNzA2NA@@._V1_UX67_CR0,0,67,98_AL_.jpg"):
                        continue

                    #Creates an Image based on bytes
                    image = Image.open(byte_stream)

                    #Converts image to PPM
                    ppmBuffer = BytesIO()
                    image.save(ppmBuffer, format='PPM')
                    ppmBuffer.seek(0)

                    #Creates the BitMap
                    bm = ppmToBitMap(ppmBuffer)

                    #List of color values
                    valueList = bm.simplify()

                    #Adds color values to the data frame
                    for i in range (len(BitMap.colors)):
                        df.loc[counter, BitMap.colors[i].name] = valueList[i]
                    df.loc[counter, 'Shade'] = bm.getGreyValue()

                    #Output for what row it is computing
                    print(counter , value)
        
        #Creates the CSV based on data frame
        df.to_csv("newCSV.csv")
    except FileNotFoundError:
        print("File not found")
    except csv.Error as error:
        print(f"CSV Error: {error}")

    #Output for program being completed
    print("Done")

main()