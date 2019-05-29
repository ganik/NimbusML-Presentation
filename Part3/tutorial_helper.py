# General imports and helper functions
import os, sys
import pandas as pd
import numpy as np
import math
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import PIL
from IPython.display import Image

def show_gallery(data, num_images=12, randomize=True, add_name=False, add_prob=False, flag_mistakes=False):
    num_images = min(num_images, len(data))
    if num_images == 0:
        print('Data length is zero. No image to show')
        return
    
    if randomize:
        data = data.sample(n=num_images)
    else:
        data = data.iloc[:num_images, :]

    if num_images <= 12:
        size = 2.5
        n_col = 6
        dpi = 300
    elif num_images > 12 and num_images <= 24:
        size = 1.5
        n_col = 10
        dpi = 300
    else:
        size = 1.5
        n_col = 10
        dpi = 100
    
    data.reset_index(inplace=True)
    image_files = data.ImagePath.values
    n_row = math.ceil(len(image_files)/n_col)
    fig = plt.figure(figsize=(size*n_col, size*n_row), dpi=dpi)
    for i in range(len(image_files)):
        ax = plt.subplot(n_row, n_col, i+1)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])        
        drop_axis = True
        if add_name and add_prob:
            name = os.path.basename(data.loc[i,'ImagePath'])
            prob =data.loc[i,'Probability']
            ax.set_xlabel('%0.5f\n%s' % (prob, name))
            drop_axis = False
        elif add_name:
            name = os.path.basename(data.loc[i,'ImagePath'])
            ax.set_xlabel(name)
            drop_axis = False
        elif add_prob:
            prob =data.loc[i,'Probability']
            ax.set_xlabel('%0.5f' % prob)
            drop_axis = False
        
        if flag_mistakes and data.loc[i, 'IsMistake']:
            drop_axis = False
            for axis in ['top','bottom','left','right']:
                ax.spines[axis].set_linewidth(5)
                ax.spines[axis].set_color('red')

        if drop_axis:
            plt.axis('off')
        plt.imshow(mpimg.imread(image_files[i]))
    plt.show()

def get_dimensions(data):
    dims = data.ImagePath.map(lambda x: PIL.Image.open(x).size)
    w, h = zip(*dims)
    return w, h

def label_counts(data, name='Data'):
    return '{} label counts:\n{}\n'.format(name, data.IsSuperman.value_counts())

def update_image_paths(df):
    if os.name == 'nt':
        # Running on windows local run
        return
    
    if 'nbuser' in df.ImagePath[0]:
        # Paths are already updated. 
        return
    
    df.ImagePath = '/home/nbuser/local/Part3/' + df.ImagePath        