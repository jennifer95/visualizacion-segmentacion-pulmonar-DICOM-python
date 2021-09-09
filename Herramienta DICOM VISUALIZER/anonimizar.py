#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 28 18:41:27 2021

@author: Jennifer Ortega

"""
from os import listdir
from os.path import isfile, join
import os
import manejo_tags as mt
import numpy as np
import pydicom

v_b = 'Entidad Anonima' # valor por default 0 
v_b1 = '' # valor por default 1

def archivo_ruta(ruta = '.'):
        try:
                x=[arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
                return x
        except IOError:
                print('La carpeta no existe')

def reescribir_valor(tag, dataset, nuevo_valor):
        id1, id2 = mt.return_id(tag[0]), mt.return_id(tag[1])
        try:
                dataset[id1,id2].value = nuevo_valor # reescribimos los datos
        except KeyError:
                        pass       

def anonimizar_img_fun(nombre_paciente_anonimo, ruta):
        """ 
        Función que anonimiza una imagen DICOM.
        nombre_paciente_anonimo: Nuevo nombre con el que se identificara(anonimizara) la imagen
        ruta: Ruta donde se encuentra la imagen.
        """
        tags = np.loadtxt('tags/private_tags.dat', delimiter= ',', dtype='str')
        with pydicom.dcmread(ruta) as dataset: # leemos la imagen
                for tag in tags:

                        if tag[0]== '0010' and tag[1]== '0010':
                                reescribir_valor(tag,dataset,nombre_paciente_anonimo)
                        elif tag[0]== '0008' and tag[1]== '0080' or tag[1]== '1050' or tag[1]== '1040':
                                reescribir_valor(tag,dataset,v_b)                       
                        elif tag[0]== '0040' and tag[1]== '2017':
                                reescribir_valor(tag,dataset, v_b1)  
                        elif tag[0]== '0010' and tag[1]== '0020':
                                reescribir_valor(tag,dataset, v_b1)                                       
                        elif tag[0]== '0018' and tag[1]== '1030':
                                pass
                        elif tag[0]== '0010' and tag[1]== '0040' or tag[1]== '1010':
                                pass
                        elif tag[0]== '0010' and tag[1]== '1040':
                                reescribir_valor(tag,dataset, v_b1)
                        else:
                                try: 
                                        tag_dato, name_dato,value_dato, keyword_dato, VR_dato, VM_dato= mt.return_data(ruta, tag[0], tag[1])
                                        if VR_dato == 'DA' or VR_dato == 'TM' or VR_dato == 'LO':
                                                pass
                                        else:
                                                reescribir_valor(tag,dataset,v_b1)
                                except KeyError:
                                        pass
                return dataset

def anonimizar_img():
        """
        Programa que anonimiza una imagen DICOM
        """
        try:
                ruta = str(input('Por favor ingrese la ruta de la imagen: '))
                nombre_paciente_anonimo = str(input('Por favor ingrese el nombre anónimo de la imagen: '))
                dataset = anonimizar_img_fun(nombre_paciente_anonimo, ruta)      
                dataset.save_as(ruta + '-A')# creamos y guardamos una nueva imagen con los datos privados modificados. 
        except:
                print('Archivo no encontrado')    

def anonimizar_paciente_fun(nombre_paciente, ruta, carpeta_salida ): 
        """ 
        Anonimiza una carpeta entera de imágenes DICOM de un solo paciente
        nombre_paciente: Nuevo nombre con el que se identificara(anonimizara) las imagenes
        path: ruta de la carpeta que se anonimizará
        """
        os.system('mkdir '+ carpeta_salida) # creamos la carpeta de salida  
        lista = os.listdir(ruta)
        for i in lista:
            original_filename = (ruta + '/' + i ) # abrimos la imagen
            dataset = anonimizar_img_fun(nombre_paciente, original_filename)                                                                  
            dataset.save_as(carpeta_salida+ '/' + i + '-A')# creamos y guardamos una nueva imagen con los datos privados modificados.
def anonimizar_paciente():
        """
        Programa que anonimíza una carpeta entera con imágenes de un paciente
        """
        try: 
                path  = str(input('Por favor ingrese la ruta de la carpeta: '))
                carpeta_salida = path + '-A'
                nombre_paciente = str(input('Por favor ingrese el nombre del paciente con el cual se identificara: '))
                anonimizar_paciente_fun(nombre_paciente, path, carpeta_salida )
        except:
                print('Archivo no encontrado')

def anonimizar_carpeta_fun(ruta):
        '''Programa que anonimiza una carpeta con varios pacientes'''
        carpeta_salida = ruta + '-A'
        os.system('mkdir '+ carpeta_salida) # creamos la carpeta de salida  
        pacientes = os.listdir(ruta)
        for paciente in pacientes: 
                carpeta_salida = ruta + '-A/' + paciente+ '-A'
                anonimizar_paciente_fun(paciente + '-A', ruta + '/'+ paciente, carpeta_salida )     

def anonimizar_carpeta():
        '''Programa que anonimiza una carpeta con varios pacientes'''
        ruta  = str(input('Por favor ingrese la ruta de la carpeta: '))    
        try:    
                anonimizar_carpeta_fun(ruta) 
        except:
                print('Archivo no encontrado') 

