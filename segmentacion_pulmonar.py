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

def marcador_interno(imagen):
    """Funcion que genera el marcador interno de un corte
    """
    marker_internal = imagen < -400 # evalua si el valor del píxel cumple o no con la condición
    marker_internal = segmentation.clear_border(marker_internal)
    marker_internal_labels = measure.label(marker_internal) # encuentra cada objeto en la imagen y los etiqueta    
    areas = [r.area for r in measure.regionprops(marker_internal_labels)] # Mide las propiedades de las regiones de imágenes etiquetadas.
    areas.sort() # ordenamos 
    # ELIMINACIÓN DE LA TRAQUEA

     # Para cortes donde solo aparece un elemento (tráquea)
    if len(areas) == 1 and areas[0]< 600:
        region = measure.regionprops(marker_internal_labels)
        for coordinates in region[0].coords:                
            marker_internal_labels[coordinates[0], coordinates[1]] = 0

    # Para cortes donde los pulmones y la tráquea tienen dimensiones similares         
    elif len(areas) == 3  and areas[0] < 600 and areas[1] < 600 and areas[2] < 600 : # eliminamos la traquea
        regiones = measure.regionprops(marker_internal_labels)
        coordenadas = [r.coords[0][0] for r in measure.regionprops(marker_internal_labels)] 
        coordenadas.sort() # ordenamos
        for region in regiones:
            if region.coords[0][0] < coordenadas[-2]: # el orden logra que solo se escoja los 2 mas grandes (correspondientes a pulomnes)
                for coordinates in region.coords:                
                    marker_internal_labels[coordinates[0], coordinates[1]] = 0


    # Para cortes donde los pulmones son mas grandes que la tráque.                     
    elif len(areas) > 2: # de los 2 pulmones
        for region in measure.regionprops(marker_internal_labels):
            if region.area < areas[-2]: # el orden logra que solo se escoja los 2 mas grandes (correspondientes a pulomnes)
                for coordinates in region.coords:                
                    marker_internal_labels[coordinates[0], coordinates[1]] = 0

    marker_internal = marker_internal_labels > 0
    return marker_internal