#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 28 18:41:27 2021

@author: Jennifer Ortega

"""
import pydicom
def return_id(tag):
    '''
        Ingresa un número de 4 digitos y retorna el número en hexadecimal.
    ''' 
    tag_hex = '0x'+ str(tag)
    return tag_hex

def return_data(ruta_imagen, tag_grupo, tag_elemento):
    '''
        Ingresa la imagen y las etiquetas, retorna el Name y el valor del elemento
    '''
    img = pydicom.dcmread(ruta_imagen)   
    id1, id2 = return_id(tag_grupo), return_id(tag_elemento)
    tag = img[id1, id2].tag
    name = img[id1, id2].name
    value = img[id1, id2].value
    keyword_dato = img[id1, id2].keyword
    VR = img[id1, id2].VR
    VM = img[id1, id2].VM
    return tag, name, value, keyword_dato, VR, VM
