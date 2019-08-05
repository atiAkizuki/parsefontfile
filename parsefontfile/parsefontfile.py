import pygame
from time import time
global pointlist
global offset
global length
global weight
global f
import argparse

def auto_int(x):
    return int(x, 0)

def pointlist_update():
    #for j in range(720):
    #    for i in range(960):
    #        if i%8 ==0:
    #            byte=f.read(1)
    #            if byte!= b"":
    #                pointlist[i][j]=int(byte[0])>>(i%8+1) & 1
    #            else:
    #                pointlist[i][j]=0

    #clear pointlist
    #start = time()
    for i in range(960):
        for j in range(720):
            pointlist[i][j]=0

    for i in range((960//length)*(720//weight)):
        read_bytes=f.read((length//8)*weight)
        for (index,byte) in enumerate(read_bytes):
            for digit in range(8):
                if byte!=b"":
                    if (byte>>(7-digit) & 1)==1:
                        x_item=(i%(960//length))*length
                        x_length=index%(length//8 if length!=12 else 2)*8
                        x_digit=digit
                        y_item=i//(960//length)*weight
                        y_length=index//(length//8 if length!=12 else 2)
                        x=x_item+x_length+x_digit
                        y=y_item+y_length
                        pointlist[x][y]=1
                    #pointlist[(i%(960//length)-1)*length+index%(length//8 if length!=12 else 2)*8+digit][i//(960//length)*weight+index//(length//8 if length!=12 else 2)]=byte>>(7-digit) & 1
                #set 0,so if error occur,it will be 0
    #stop = time()
    #print(str(stop-start) + "秒")
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to read')
    parser.add_argument('-l',type=int,help='font length,default equal 24',default=24)
    parser.add_argument('-w',type=int,help='font weight,default equal 24',default=24)
    parser.add_argument('-o',type=auto_int,help='font file offset,default is 0x0',default=0x0)
    args = parser.parse_args()
    file=args.file
    offset=args.o
    length=args.l
    weight=args.w
    #file="rmZK32M.BIN"
    #offset=0x7fff
    #offset=0
    #read length==12,set length=16
    #length=24
    #weight=24
    size=[960,720]
    pointlist=[[0]*720 for i in range(960)]

    f=open(file, "rb")
    f.seek(offset)

    pointlist_update()
    pygame.init()


    screen=pygame.display.set_mode(size)
 
    pygame.display.set_caption("ParseFontFile")
    done=False
    clock=pygame.time.Clock()

    black    = (   0,   0,   0)
    white    = ( 255, 255, 255)
    color=black

    while done==False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            if event.type ==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN: #press enter
                    pointlist_update()

                if event.key==pygame.K_ESCAPE: #press esc
                    done=True
        screen.fill(white)
        for i in range(960):
            for j in range(720):
                if pointlist[i][j]==1:
                    color=black
                else:
                    color=white
                screen.set_at((i,j), color)
                #screen.set_at((i,j), black if pointlist[i][j]==1 else white)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


