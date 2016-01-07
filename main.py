
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
import scipy as sp
import pylab as pl


import math
import sys,getopt
import random

# Some Global Vars for Adjustments

# Sobel Matrix
sx = [[1,0,-1],[2,0,-2],[1,0,1]]
sy = [[1,2,1],[0,0,0],[-1,-2,-1]]

factor = 7 #Enlarge Image by Factor    
windowSize = 3 # Create w x w Box
windowStep = int(math.floor(windowSize/2)) # +- for Window Size

def myTan(x,y):
    
    if (x >= 0):
        return math.atan(y/x)
    if ((x < 0) and (y >= 0)):
        return (math.atan(y/x) + math.pi)
    if ((x < 0) and (y < 0)):
        return (math.atan(y/x) - math.pi)
    
# Based on http://jmit.us.edu.pl/cms/jmitjrn/22/28_Wieclaw_4.pdf
def getLocalOrientation(sobelx, sobely,x,y):
    
    vx = 0
    vy = 0
    angle = 0
    
    gx = 0
    gy = 0
    
    gxx = 0
    gyy = 0
    gxy = 0
    
    
    for xi in range (x-windowStep,x+windowStep):
        for yi in range (y-windowStep,y+windowStep):
            gx = sobelx[xi][yi]
            gy = sobely[xi][yi]
            
            gxx += (gx*gx)
            gyy += (gy*gy)
            gxy += gx*gy
            
        
    angle = 0.5 * myTan(gxx - gyy, 2 * gxy)
    
    if (angle <= 0):
        angle += 0.5* math.pi
    else:
        angle -= 0.5*math.pi
    
    
    '''
    k = 0
    if(phi < 0 and vx < 0):
        k = 0.5
    
    if(phi < 0 and vx >= 0):
        k = 1
    
    if(phi >= 0 and vx <=0):
        k = 0
        
    angle = phi + k * math.pi
    '''
    
    return angle
    
    
    
def drawLine(angle, x,y, draw):
    # Draw Boxes
    draw.line((x*factor, (y)*factor, (x+windowSize)*factor, (y)*factor), fill="blue")
    draw.line((x*factor, (y+windowSize)*factor, (x+windowSize)*factor, (y+windowSize)*factor), fill="blue")
    
    draw.line((x*factor, (y)*factor, (x)*factor, (y+windowSize)*factor), fill="blue")
    draw.line(((x+windowSize)*factor, (y)*factor, (x+windowSize)*factor, (y+windowSize)*factor), fill="blue")
    
    if (angle*180/math.pi != 90):
    #if (angle != 0):

        # Draw Line with angle
        linelenght = windowSize * factor / 1.5
        startx = (x+1) * factor + (factor / 2)
        starty = (y+1) * factor + (factor / 2)
        endx = math.ceil(startx + linelenght * math.sin(angle))
        endy = math.ceil(starty + linelenght * math.cos(angle))

        draw.line((startx,starty,endx,endy),fill="red",width=2)
        draw.rectangle([(startx-1,starty-1), (startx+1,starty+1)], fill="green")
        
        

def main(argv):
    
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:
        print 'main.py -i <inputfile> '
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
    print 'Input file is: ', inputfile
    
        
    im_original = Image.open(inputfile)
    
    enh = ImageEnhance.Contrast(im_original)
    im_original = enh.enhance(1)
    
    im = im_original.convert('RGB')
    pixels = im.load() 
    width, height = im.size
    
    #Calculate Mean for each Pixel (grey Value)
    pixelsMean = []
    for x in xrange(0, width):
        line = []
        for y in xrange(0, height):
            line.append(np.mean(pixels[x,y]))
        pixelsMean.append(line)
    
    

    # Draw Area for Orientation lines
    #fp = Image.new("RGB", (width*factor, height*factor), "white")
    fp = im.resize((width*factor, height*factor))
    draw = ImageDraw.Draw(fp)
    
    

    # Calculate full Sobel
    sobelx = [[0 for y in range(height)] for x in range(width)]
    sobely = [[0 for y in range(height)] for x in range(width)]
    
    maxSobel = 0
    
    for x in xrange(1, width - 2):
        for y in xrange(1, height - 2 ):
            
            # Sobel X
            tempx = 0
            tempx += sx[0][0] * pixelsMean[x-1][y-1]
            tempx += sx[0][1] * pixelsMean[x][y-1]
            tempx += sx[0][2] * pixelsMean[x+1][y-1]
            tempx += sx[1][0] * pixelsMean[x-1][y]
            tempx += sx[1][1] * pixelsMean[x][y]
            tempx += sx[1][2] * pixelsMean[x+1][y]
            tempx += sx[2][0] * pixelsMean[x-1][y+1]
            tempx += sx[2][1] * pixelsMean[x][y+1]
            tempx += sx[2][2] * pixelsMean[x+1][y+1]
            
            
            # Sobel y
            tempy = 0
            tempy += sy[0][0] * pixelsMean[x-1][y-1]
            tempy += sy[0][1] * pixelsMean[x][y-1]
            tempy += sy[0][2] * pixelsMean[x+1][y-1]
            tempy += sy[1][0] * pixelsMean[x-1][y]
            tempy += sy[1][1] * pixelsMean[x][y]
            tempy += sy[1][2] * pixelsMean[x+1][y]
            tempy += sy[2][0] * pixelsMean[x-1][y+1]
            tempy += sy[2][1] * pixelsMean[x][y+1]
            tempy += sy[2][2] * pixelsMean[x+1][y+1]
            
            
            if (tempx == tempy):
                if(bool(random.getrandbits(1))):
                    if(bool(random.getrandbits(1))):
                        tempx += 1
                    else:
                        tempx -= 1
                else:
                    if(bool(random.getrandbits(1))):
                        tempy += 1
                    else:
                        tempy -= 1
                    
            if (tempx == 0):
                if(bool(random.getrandbits(1))):
                    tempx += 1
                else:
                    tempy -= 1
            
            if (tempy == 0):
                if(bool(random.getrandbits(1))):
                    tempy += 1
                else:
                    tempy -= 1
                
            
            sobelx[x][y] = tempx
            sobely[x][y] = tempy
        
            sobel = int(math.sqrt(tempx*tempx + tempy*tempy))
            if (sobel > maxSobel):
                maxSobel = sobel

    for x in xrange(1, width - 2):
        for y in xrange(1, height - 2 ):       
            
            sobel = math.sqrt(sobelx[x][y]*sobelx[x][y] + sobely[x][y]*sobely[x][y])
            
            color = 0.0
            color = int(math.ceil(sobel / maxSobel * 255))

            #draw.rectangle([(x*factor,y*factor), ((x+1)*factor,(y+1)*factor)], fill=(color,color,color))
            
    
    # Get Orientation based on Sobel Gradients in a w x w Window
    for x in xrange(windowStep, width - windowStep, windowSize):
        for y in xrange(windowStep, height - windowStep, windowSize):
            angle = getLocalOrientation(sobelx, sobely, x, y)
            drawLine(angle,x,y, draw)

        
                
    # Show Image        
    fp.show()
    
    
if __name__ == "__main__":
    main(sys.argv[1:])



    
