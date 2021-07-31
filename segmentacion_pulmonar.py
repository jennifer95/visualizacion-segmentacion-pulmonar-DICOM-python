#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu June 25 10:51:08 2021

@author: Jennifer Ortega

"""
import pydicom
import numpy as np
import matplotlib.pylab as plt
import imprimir_imagen as imp
import scipy.ndimage as ndimage
import os

from skimage import measure, morphology, segmentation

def image_gradiente(image):
    'Funcion que crea la imagen grediente de una imagen de entrada'
    sobel_dx = ndimage.sobel(image, 1)
    sobel_dy = ndimage.sobel(image, 0)
    sobel_gradient = np.hypot(sobel_dx, sobel_dy) # calculamos el norma
    sobel_gradient *= 255.0 / np.max(sobel_gradient) # normalizamos
    return sobel_gradient