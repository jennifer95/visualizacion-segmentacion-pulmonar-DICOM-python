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
    """
    Función que crea la imagen gradiente de una imagen de entrada
    """
    sobel_dx = ndimage.sobel(image, 1)
    sobel_dy = ndimage.sobel(image, 0)
    sobel_gradient = np.hypot(sobel_dx, sobel_dy)  # se calcula la norma
    sobel_gradient *= 255.0 / np.max(sobel_gradient) # se normaliza
    return sobel_gradient

def marcador_interno(imagen):
    """
    Función que genera el marcador interno de un corte
    """
    marker_internal = imagen < -400 # evalua si el valor del píxel cumple o no con la condición
    marker_internal = segmentation.clear_border(marker_internal)
    marker_internal_labels = measure.label(marker_internal) # encuentra cada objeto en la imagen y los etiqueta  
    
    # ELIMINACION DE ESTRUCTURAS PEQUEÑAS
    for region in measure.regionprops(marker_internal_labels):
        if region.area < 70:
            for coordinates in region.coords:                
                marker_internal_labels[coordinates[0], coordinates[1]] = 0
                
    # ELIMINACIÓN DE LA TRAQUEA    
    areas = [r.area for r in measure.regionprops(marker_internal_labels)] # Mide las propiedades de las regiones de imágenes etiquetadas.
    areas.sort() # se ordenan las regiones

     # Para cortes donde solo aparece un elemento (tráquea)
    if len(areas) == 1 and areas[0]< 500:
        region = measure.regionprops(marker_internal_labels)
        for coordinates in region[0].coords:                
            marker_internal_labels[coordinates[0], coordinates[1]] = 0

    # Para cortes donde los pulmones y la tráquea tienen dimensiones similares         
    elif len(areas) == 3  and areas[0] < 300 and areas[1] < 300 and areas[2] < 300 : # se elimina la traquea
        regiones = measure.regionprops(marker_internal_labels)
        coordenadas = [r.coords[0][0] for r in measure.regionprops(marker_internal_labels)] 
        coordenadas.sort() # se ordenan las regiones
        for region in regiones:
            if region.coords[0][0] < coordenadas[-2]: # el orden logra que solo se escoja los 2 más grandes (correspondientes a pulmones)
                for coordinates in region.coords:                
                    marker_internal_labels[coordinates[0], coordinates[1]] = 0


    # Para cortes donde los pulmones son más grandes que la tráquea.                     
    elif len(areas) > 2: # de los 2 pulmones
        for region in measure.regionprops(marker_internal_labels):
            if region.area < areas[-2]: # el orden logra que solo se escoja los 2 mas grandes (correspondientes a pulmones)
                for coordinates in region.coords:                
                    marker_internal_labels[coordinates[0], coordinates[1]] = 0
                    
    if len(areas) == 2 and areas[0] < 300 and areas[1] < 300:
        l =[]
        for region in measure.regionprops(marker_internal_labels):
            coordinates = region.coords
            l.append(coordinates[0][0])
        if abs(l[0]-l[1])> 30:
            for region in measure.regionprops(marker_internal_labels): 
                for coordinates in region.coords:                
                    marker_internal_labels[coordinates[0], coordinates[1]] = 0
                break                    

    marker_internal = marker_internal_labels > 0
    return marker_internal



def marcador_externo(imagen, iterations_a=10, iterations_b=55):
    """
    Función que genera el marcador externo de un corte
    """
    marker_internal = marcador_interno(imagen)
    external_a = ndimage.binary_dilation(marker_internal, iterations=iterations_a)
    external_b = ndimage.binary_dilation(marker_internal, iterations=iterations_b)
    marker_external = external_b ^ external_a
    return marker_external

def marcadores(imagen):
    """
    Función que genera el marcador watershed de un corte
    """
    marker_internal = marcador_interno(imagen)
    marker_external = marcador_externo(imagen)
    marker_watershed = np.zeros((512, 512), dtype=int)
    marker_watershed += marker_internal * 255
    marker_watershed += marker_external * 128
    return marker_internal, marker_external, marker_watershed

def seg_watershed(imagen,iterations_black = 6 ):
    """
    Función para segmentar pulmones, mediante el ingreso de una imagen en escala de grises.
    """
    imagen_grad = image_gradiente(imagen)
    marker_internal, marker_external, marker_watershed = marcadores(imagen)
    watershed = segmentation.watershed(imagen_grad, marker_watershed)
    outline = ndimage.morphological_gradient(watershed, size=(3,3))
    outline = outline.astype(bool)
    blackhat_struct = [[0, 0, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0]]
    # se crea el elemento estructurante
    blackhat_struct = ndimage.iterate_structure(blackhat_struct, iterations_black )
    outline += ndimage.black_tophat(outline, structure = blackhat_struct)
    lungfilter = np.bitwise_or(marker_internal, outline)
    lungfilter = ndimage.morphology.binary_closing(lungfilter, structure=np.ones((5,5)), iterations=3)
    segmented = np.where(lungfilter == 1, imagen, -2000*np.ones((512, 512)))
    return segmented
def seg_examen(ruta, interaciones):
    """
    Función que realiza la segmentación de pulmones de un examen completo de CT, mediante archivos DICOM de entrada
    """
    imagen = imp.remov_cama(imp.extrac_matrix(imp.load_scan(ruta)))                       
    segmentacion = np.stack([ seg_watershed(corte, 4) for corte in imagen]) 
    segmentacion = segmentacion.astype(np.int16)
    return segmentacion 

def seg_imagen_matriz(imagen, interaciones):
    """
    Función que realiza una segmentacion depulmones mediante una una matriz de entrada
    """
    segmentacion = np.stack([ seg_watershed(corte, 4) for corte in imagen]) 
    segmentacion = segmentacion.astype(np.int16)
    return segmentacion 

    
    
    
    
    
