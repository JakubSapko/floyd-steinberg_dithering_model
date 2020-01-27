import os
from PIL import Image
from math import floor
from argparse import ArgumentParser


class dithered_image():
    def __init__(self, p, alg = None, output = None):
        self.p = self.get_p(p)
        self.alg = alg
        self.output = output
        self.func = self.get_f(self.alg)
        self.func(self.p)


    def find_closest(self, value):
        return 255*floor(value/128)

    def algo(self, imgf):
        nimg = Image.open(imgf)
        nimg = nimg.convert('RGB')
        pixel = nimg.load()
        xlim, ylim = nimg.size
        for y in range(1, ylim):
            for x in range(1, xlim):
                red_old_pixel, green_old_pixel, blue_old_pixel=pixel[x, y]

                red_new_pixel=self.find_closest(red_old_pixel)
                green_new_pixel=self.find_closest(green_old_pixel)
                blue_new_pixel=self.find_closest(blue_old_pixel)
                pixel[x,y] = red_new_pixel, green_new_pixel, blue_new_pixel

                rerror = red_old_pixel - red_new_pixel
                berror = blue_old_pixel - blue_new_pixel
                gerror = green_old_pixel - green_new_pixel

                if x<xlim-1:
                    r = pixel[x+1, y][0] + round(rerror*7/16)
                    g = pixel[x+1, y][1] + round(gerror*7/16)
                    b = pixel[x+1, y][2] + round(berror*7/16)
                    pixel[x+1, y] = (r,g,b)
                
                if x>1 and y<ylim-1:
                    r = pixel[x-1, y+1][0] + round(rerror*3/16)
                    g = pixel[x-1, y+1][1] + round(gerror*3/16)
                    b = pixel[x-1, y+1][2] + round(berror*3/16)
                    pixel[x-1, y+1] = (r,g,b)

                if y<ylim-1:
                    r = pixel[x, y+1][0] + round(rerror*5/16)
                    g = pixel[x, y+1][1] + round(gerror*5/16)
                    b = pixel[x, y+1][2] + round(berror*5/16)
                    pixel[x, y+1] = (r,g,b)

                if x<xlim-1 and y<ylim-1:
                    r = pixel[x+1, y+1][0] + round(rerror*1/16)
                    g = pixel[x+1, y+1][1] + round(gerror*1/16)
                    b = pixel[x+1, y+1][2] + round(berror*1/16)
                    pixel[x+1, y+1] = (r,g,b)
        if self.output:
            nimg.save(self.output)
        else:
            nimg.show()

    def get_p(self, p):
        if p.startswith('/') and not p.startswith('~/'):
            return os.getcwd() + '/' + p
        else: return p
    
    def get_f(self, alg):
        return self.algo

def main():
    pars = ArgumentParser(description="Floyd-Steinberg image dithering")
    pars.add_argument("image_path", help='Provide image localization')
    pars.add_argument("-o", help="Output image localization")
    arguments = pars.parse_args()
    if arguments.image_path and not arguments.o:
        dithered_image(arguments.image_path)
    elif arguments.image_path and arguments.o:
        dithered_image(arguments.image_path, output=arguments.o)


main()        
#C:\Users\jakub\Desktop\floydsteinberg.py



