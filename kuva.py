from progress.bar import Bar
from PIL import Image
import numpy as np
import statistics
import matplotlib.pyplot as plt

# Print width in millimeters. For some reason Adobe illustrator has weird
# conversion ratio between mm and px.
print_width_mm = 26
px_per_mm = 2.8346538461538461538461538461538
print_width_px = round(print_width_mm * px_per_mm)

# Open image and ensure RGB

im = Image.open("L:\Painokone\Tarjouksia ja tilauksia\Suomen PV\FF5493_toisto.tif_ PV colors leveys skaalattu 640.png").convert('RGB')
#im = Image.open("L:\Painokone\Tarjouksia ja tilauksia\Viron PV\camo tumma 800 mm-02.png").convert('RGB')
#im = Image.open("L:\Painokone\Tarjouksia ja tilauksia\Suomen PV\FF5493_toisto.tif_ PV colors-01.png").convert('RGB')
#im = Image.open("L:\Painokone\Tarjouksia ja tilauksia\Suomen PV\FF5493_toisto 800 mm 2 artboards-01.png").convert('RGB')
#im = Image.open("L:\Painokone\Tarjouksia ja tilauksia\Viron PV\camo tumma 800 mm-02.png").convert('RGB')

# Make into Numpy array
na = np.array(im)
 
# Get colors and corresponding counts
colors, counts = np.unique(na.reshape(-1,3), axis=0, return_counts=1)
print("\nWhole image color distribution:")

i = 0
for x in counts:
    print("Color (R",str(colors[i,0]).zfill(3), " G",str(colors[i,1]).zfill(3), " B", colors[i,2],")", x,x/sum(counts))
    i = i + 1

im_stdevs = np.empty(im.size[0]-print_width_px)

# Progress bar
with Bar('Processing...', max=im.size[0] - print_width_px) as bar:

    # Iterate through all possible locations for print width.
    for x in range(im.size[0] - print_width_px):

        crop_rectangle = (x, 0, x + print_width_px, im.size[1])
        im_cropped = im.crop(crop_rectangle)
    
        # Make into Numpy array
        na = np.array(im_cropped)
        
        # Get colors and corresponding counts
        colors, counts = np.unique(na.reshape(-1,3), axis=0, return_counts=1)
        
        im_stdevs[x] = statistics.stdev(counts)
        
        bar.next()

plot_title = "standard deviations"#" of colors for " + str(print_width_mm) + " mm print width"
plt.xlabel("print area top-left corner x-value") 
plt.ylabel("standard deviation of colors") 
plt.title(plot_title)
plt.plot(np.arange(im_stdevs.size), im_stdevs)
plt.show()

print("Minimum stdev: x =", np.argmin(im_stdevs),"px (", np.argmin(im_stdevs)/px_per_mm, " mm) for print width", print_width_mm, "mm. Stdev", min(im_stdevs))
        