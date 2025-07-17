import numpy as np
from PIL import Image

def recolor_image(file_name):
    im = Image.open(file_name + '.png')
    data = np.array(im)

    r1, g1, b1 = 0, 0, 0 # Original value
    r2, g2, b2 = 136, 8, 8 # Value that we want to replace it with

    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save(file_name + '.png')

path = "assets/logos/"

images = ["assamite", "brujah", "gangrel", "hecata",
          "lasombra", "malkavian", "ministry", "nosferatu",
          "ravnos", "toreador", "tremere", "tzimisce",
          "ventrue", "salubri", "caitiff", "vtm"]

for image in images:
    recolor_image(path+image)
