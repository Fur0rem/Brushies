import os
import cv2
import numpy as np
from PIL import Image

def make_gif(save_path, images):
    os.makedirs("brush_gifs", exist_ok=True)
    images[0].save(f"brush_gifs/{save_path}.gif", save_all=True, append_images=images[1:], optimize=False, duration=20, loop=0, disposal=2)
    os.system(f"gifsicle -O3 --colors 256 brush_gifs/{save_path}.gif -o brush_gifs/{save_path}.gif")

x_offset_map=[0,1,4,2,1,0]

brusheds = [("intensa", (55, 50, 255)),
            ("weenside", (255, 25, 0)),
            ("charz", (255, 0, 25)),
            ("microwave", (255, 255, 0)),
            ("joey", (255, 255, 255)),
            ("arcanin", (0, 100, 255)),
            ("tygore", (255, 0, 100)),
            ("agsilver", (20, 255, 50)),
            ("peter", (255, 20, 100)),
            ("karawii", (0, 255, 0)),
            ("paultam", (255, 0, 0)),
            ("sigma", (20, 20, 255)),
            ("smiffy", (105, 40, 255)),
            ("zimc", (150, 30, 150)),
            ("troy", (100, 0, 255)),
            ("zach", (255, 0, 0)),
            ("void", (60, 60, 60)),
            ("ryu", (255, 200, 60)),
            ("voltren", (250, 10, 55)),
            ("cinny", (200, 70, 70)),
            ("qKitti", (50, 20, 150)),
            ("boi", (90, 190, 190)),
            ("dank", (180, 180, 180)),
            ("nooby",(255, 200, 60)),
            ("yrax", (200, 70, 70)),
            ("sycro",(40,190,200)),
            ("cobalium",(255,20,100)),
            ("infra",(100,150,250)),
            ("silver",(250,200,50)),
            ("samiversal",(0,100,30)),
            ("globron",(250,180,10)),
            ("rubix", (255,80,255)),
            ("kale", (255,80,255)),
            ("majax", (55, 50, 255)),
            ("toughfey", (200, 150, 0)),
          ] 

brush_frames = [cv2.imread(str(f"brush_frames/{i}.png"), cv2.IMREAD_UNCHANGED) for i in range(1,6+1)]

for (brushed, (r, g, b)) in brusheds :

    # Load the brushed image
    print(f"Processing {brushed}")
    image = cv2.imread(str(f"brushed/{brushed}.png"), cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

    # For each pixel, cramp the alpha to 0 or 255
    for y in range(len(image)):
        for x in range(len(image)):
            if image[y][x][3] > 128:
                image[y][x][3] = 255
            else:
                image[y][x][3] = 0

    images = []    
    for i in range(1,6+1):
        
        new_pixels = np.empty((len(image), len(image), 4), dtype=np.uint8)
        brush_image = brush_frames[i-1]
        
        # Offset the image by the x_offset_map for the animation
        for y in range(len(new_pixels)):
            for x in range(len(new_pixels)):
                if (x - x_offset_map[i-1]) < 0:
                    continue
                  
                new_pixels[y][x] = image[y][x-x_offset_map[i-1]]
                
        # Apply the brush to the image
        for y in range(len(new_pixels)):
            for x in range(len(new_pixels)):
                if ((pix := (brush_image[y][x])) != [0,0,0,0]).any():
                    # Multiplicative blending for colour
                    rt = pix[0] * (r/255.0)
                    gt = pix[1] * (g/255.0)
                    bt = pix[2] * (b/255.0)
                    new_pix = [int(rt), int(gt), int(bt), pix[3]]
                    new_pixels[y][x] = new_pix
        
        # Convert the numpy array to a PIL image
        im = Image.fromarray(np.array(new_pixels).astype('uint8')).convert("RGBA")
        images.append(im)

    make_gif(brushed, images)