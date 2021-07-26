#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 18:41:27 2021

@author: Jennifer Ortega

"""
import pydicom
import numpy as np
import matplotlib.pylab as plt
import os
from PIL import Image

def get_pixel_hu(image, intercept, slope):
    '''Función recibe la  matriz de píxeles DICOM, el interceto y el slope y devuele la matriz en unidades Hounsfield'''
    image[image == -2000] = 0
    if slope != 1:
        image = slope * image
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)

def extract_m_i_s(ruta_imagen):
    '''Funcion que extrae la matrix de pixeles el slope y el intercetp'''
    archivo_dicom = pydicom.dcmread(ruta_imagen)
    intercept = archivo_dicom.RescaleIntercept
    slope = archivo_dicom.RescaleSlope
    image = archivo_dicom.pixel_array
    return image, intercept, slope

def visualizar_pantalla_fun(matriz,nombre_img, aspect=1, vdpi = 1, minimo=-100, maximo=300):
    '''Función que recibe una ruta de un archivo DICOM y devuelve la imagen en pantalla y la guarda'''
    fig, ax = plt.subplots()
    ax.imshow(matriz ,cmap=plt.cm.gray, vmin = minimo, vmax =maximo)
    ax.axis('off')
    ax.set_aspect(aspect)
    fig.savefig(nombre_img, dpi=vdpi,bbox_inches='tight', pad_inches = 0)
    plt.show()

def visualizar_pantalla():
    '''Función que grafica una imagen de TC y la guarda'''
    ruta_imagen = str(input('Por favor ingrese el nombre de la imagen o la ruta donde se encuentra la imagen: '))
    nombre_img = str(input('Por favor ingrese el nombre de la imagen que se guardará: '))
    image, intercept, slope = extract_m_i_s(ruta_imagen)
    visualizar_pantalla_fun(get_pixel_hu(image, intercept, slope),nombre_img, 1, 500)

def load_scan(path):
    '''FUnción que lee una carpeta de un paciente y retorna todas las imagenes en formato np.ndarray con todas las imagenes en unidades HU'''
    slices = [pydicom.dcmread(path + '/' + s) for s in os.listdir(path)] # leemos los archivos
    slices.sort(key = lambda x: int(x.InstanceNumber)) # ordenamos de acuerdo a InstanceNumber
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices

def extrac_matrix(slices):
    '''Extrae la matriz de slices que es una lista con archivos dicom leidad con pydicom un objeto pydicom.dataset.FileDataset
     y las devielde en unidades Hu '''
    intercept = slices[0].RescaleIntercept
    slope = slices[0].RescaleSlope  
    image = np.stack([s.pixel_array for s in slices]) # junta todos los pixel array en uno solo 
    image = image.astype(np.int16) # convertimos en una sola matriz  
    image = get_pixel_hu(image, intercept, slope)
    return image

def remov_cama(image, y1 = 350 ,y2= 512):
    '''Funcion que permite remover la camilla de un examen de TC'''
    for i in range(0,len(image)):
        image[i][y1:y2,:]=-1024
    return image

def slices_to_image(ruta_imagen, min_filas, nombre_img, tipo_plano= 'axial', porc = 100):
    '''Función que grafica imágenes  de un examen de TC'''
    #imgs = remov_cama(extrac_matrix(load_scan(ruta_imagen)))
    imgs = extrac_matrix(load_scan(ruta_imagen))
    if tipo_plano == 'axial':
        n = len(imgs) 
        if n > 200 and n < 400:
            imgs = [imgs[i,:,:] for i in range(1,len(imgs), 4) ]
        if n > 400:
            imgs = [imgs[i,:,:] for i in range(1,len(imgs), 8) ]
        n = len(imgs)
        for i in range(min_filas, n+1, 1):
            if i == n:
                imgs = imgs[0:n-1]
                n = len(imgs)  
                for i in range(min_filas, n+1):
                    if n%i == 0 :
                        m = int(n/i)
                        xa = []
                        for l in range(m,n+1,m):
                            xa.append(np.concatenate(imgs[l-m:l], axis=1))
                        break 
            else:
                if n%i == 0 :
                    m = int(n/i)
                    xa = []
                    for l in range(m,n+1,m):
                        xa.append(np.concatenate(imgs[l-m:l], axis=1))
                    break
        return np.concatenate(xa, axis=0), m,n

    elif tipo_plano == 'sagital':
        n = imgs.shape[2]
        inicio = int(n/2- (porc*n/200))
        final = int(n/2 +(porc*n/200))
        imgs = imgs[:,:,inicio : final]
        n = imgs.shape[2]
        for i in range(min_filas, n+1):
            if i == n:
                imgs = imgs[:,:,0:n-1]
                n = len(imgs)  
                for i in range(min_filas, n+1):
                    if n%i == 0 :
                        m = int(n/i)
                        xa = []
                        for l in range(m,n+1,m):
                            xa.append(np.concatenate(imgs[:,:,l-m:l].T, axis=1))
                        break 
            else:
                if n%i == 0 :
                    m = int(n/i)
                    xa = []
                    for l in range(m,n+1,m):
                        xa.append(np.concatenate(imgs[:,:,l-m:l].T, axis=1))
                    break
        return np.concatenate(xa, axis=0), m,n
 
    elif tipo_plano == 'coronal':
        n = imgs.shape[1]
        inicio = int(n/2- (porc*n/200))
        final = int(n/2 +(porc*n/200))
        imgs = imgs[:,inicio : final,:]
        n = imgs.shape[1]
        for i in range(min_filas, n+1):
            if i == n:
                imgs = imgs[:,0:n-1,:]
                n = len(imgs)  
                for i in range(min_filas, n+1):
                    if n%i == 0 :
                        m = int(n/i)
                        xa = []
                        for l in range(m,n+1,m):
                            s = [imgs[:,i,:] for i in range(l-m, l) ]
                            xa.append(np.concatenate(s,  axis=1))
                        break 
            else:
                if n%i == 0 :
                    m = int(n/i)
                    xa = []
                    for l in range(m,n+1,m):
                        s = [imgs[:,i,:] for i in range(l-m, l) ]
                        xa.append(np.concatenate(s,  axis=1))
                    break
        return np.concatenate(xa, axis=0), m,n
 

def visualizar_pantalla_mult_cor_fun(ruta_imagen, min_filas, nombre_img, vdpi, minimo = -100, maximo= 300):
    slices = load_scan(ruta_imagen)
    ss = slices[0].SliceThickness # calculamos la distancia entre slices
    ps = slices[0].PixelSpacing #distancia entre píxeles
    ax_aspect = ps[1]/ps[0]
    sag_aspect = ss/ps[1]
    cor_aspect = ss/ps[0]
    matrix,m,n = slices_to_image(ruta_imagen, min_filas, nombre_img, 'coronal', 6.25)
    visualizar_pantalla_fun(matrix,nombre_img, cor_aspect, 1000  , minimo , maximo) 

def visualizar_pantalla_mult_sag_fun(ruta_imagen, min_filas, nombre_img, vdpi, minimo = -100, maximo= 300):
    slices = load_scan(ruta_imagen)
    ss = slices[0].SliceThickness # calculamos la distancia entre slices
    ps = slices[0].PixelSpacing #distancia entre píxeles
    ax_aspect = ps[1]/ps[0]
    sag_aspect = ss/ps[1]
    cor_aspect = ss/ps[0]
    matrix , m , n = slices_to_image(ruta_imagen, min_filas, nombre_img, 'sagital', 6.25)
    visualizar_pantalla_fun(matrix,nombre_img, 1/sag_aspect, 1000  , minimo, maximo)

def visualizar_pantalla_mult_ax_fun(ruta_imagen, min_filas, nombre_img, vdpi, minimo = -100, maximo= 300):
    matrix,m,n = slices_to_image(ruta_imagen, min_filas, nombre_img, 'axial', 100)
    visualizar_pantalla_fun(matrix,nombre_img, 1, 2000  , minimo, maximo) 
    image = Image.open(nombre_img)
    new_image = image.resize((m*512, int(n/m)*512))  
    new_image.save(nombre_img)
                

def visualizar_pantalla_mult(tipo_plano):
    '''Función que grafica imágenes  de un examen de TC'''
    ruta_imagen = str(input('Por favor ingrese la ruta donde se encuentra la carpeta del paciente: '))
    min_filas = int(input('Por favor ingrese el número mínimo de filas para el visualización: '))
    nombre_img = str(input('Por favor ingrese el nombre de la imagen que se guardará: '))
    if tipo_plano == 'axial':
        visualizar_pantalla_mult_ax_fun(ruta_imagen, min_filas, nombre_img, 2000)
    elif tipo_plano == 'coronal':
        visualizar_pantalla_mult_cor_fun(ruta_imagen, min_filas, nombre_img, 2000)
    elif tipo_plano == 'sagital':
        visualizar_pantalla_mult_sag_fun(ruta_imagen, min_filas, nombre_img, 2000)
        
def muestra_datos(stack, rows=5, cols=5, start_with=10, show_every=1, minimo = -100, maximo=300 ):
    """Funcion que grafica las imágenes a partir de una matriz de 3 dimensiones"""
    fig,ax = plt.subplots(rows,cols,figsize=[10,10])
    for i in range(rows*cols):
        ind = start_with + i*show_every
        ax[int(i/rows),int(i % rows)].set_title('Corte %d' % ind)
        ax[int(i/rows),int(i % rows)].imshow(stack[ind],cmap=plt.cm.gray, vmin=minimo, vmax=maximo)
        ax[int(i/rows),int(i % rows)].axis('off')
    plt.show()        







