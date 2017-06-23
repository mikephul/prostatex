import tensorflow as tf
import numpy as np
import math
# import timeit
import random
import matplotlib.pyplot as plt
import scipy.io as sio
# from scipy import ndimage
# from copy import copy

# matfile: file of matlab cell. The variable name in matlab is as same as filename **very important**
# data is height x width x depth
# try to keep the annotated coordinate in the center. If not possible, only keep it in the image. 
def crop_data(matfile, coordinate_file, height=50, width=50, depth=12):
    # Matlab cell containing images
    matcell = sio.loadmat(matfile)
    cell_key = matfile.split('.')[0].split('/')[-1]
    matcell = matcell[cell_key][0]
    
    # Matlab array containing annotated coordinates
    matco = sio.loadmat(coordinate_file)
    matco_key = coordinate_file.split('.')[0].split('/')[-1]
    matco = matco[matco_key]
    num_patients,_,_ = matco.shape
    
    cropped = np.zeros((num_patients, height, width, depth))
    
    for i in range(num_patients):
        image = matcell[i]
        img_height, img_width, img_depth = image.shape
        assert height <= img_height
        assert width <= img_width
        assert depth <= img_depth
        co = matco[i][0]
        
        # Get ranges
        start_height, stop_height = get_range(co[0], height, img_height)
        start_width, stop_width = get_range(co[1], width, img_width)
        start_depth, stop_depth = get_range(co[2], depth, img_depth)
        
        # Crop images
        cropped[i,:,:,:] = matcell[i][start_height:stop_height, start_width:stop_width, start_depth:stop_depth]
    
    return cropped

def get_range(co, size, full):
    if co - size//2 > 0:
        if co + size//2 < full:
            start = co - size//2
            stop = start + size
        else:
            stop = full
            start = full - size
    else: 
        start = 0
        stop = size
    return start, stop