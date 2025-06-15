import os
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, filters, io, color, util, feature
from scipy import ndimage as ndi

if __name__ == '__main__':
    print("hello from utils.py")
    img = io.imread('images/2b2t_rick.png', as_gray = True)

    print("Image shape:", img.shape)
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    ax.set_title('Lichtenstein Test Image')
    plt.imshow(img, cmap='gray')
    plt.show()
    