#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 28 18:41:27 2021

@author: Jennifer Ortega

"""
from pprint import pprint
from datetime import datetime
import numpy as np
import pydicom
import manejo_tags 
import verificar
import endex

def print_data(tag_dato, name_dato, value_with_units, keyword_dato, VR_dato, VM_dato):
        """
        Imprime de forma ordenada los valores ingresados
        """
        space = ''
        if len(name_dato)>=40 and len(keyword_dato)>=35:
                print(f'{str(tag_dato):>12s}{name_dato[0:38]:>40s} {str(keyword_dato[0:33]):>35s} {str(value_with_units):>48s}')  
                print(f'{space:>12s}{name_dato[38:len(name_dato)]:>40s} {keyword_dato[33:len(keyword_dato)]:>35s} {space:>48s}') 
        elif len(name_dato)>=40:     
                print(f'{str(tag_dato):>12s}{name_dato[0:38]:>40s} {str(keyword_dato):>35s} {str(value_with_units):>48s}')  
                print(f'{space:>12s}{name_dato[38:len(name_dato)]:>40s} {space:>35s} {space:>48s}') 
        elif len(value_with_units)>= 48:
                print(f'{str(tag_dato):>12s}{name_dato:>40s} {str(keyword_dato):>35s} {str(value_with_units[0:46]):>48s}')  
                print(f'{space:>12s}{name_dato[28:len(name_dato)]:>40s} {space:>35s} {str(value_with_units[46:len(value_with_units)]):>48s}') 
        else:
                print(f'{str(tag_dato):>12s}{name_dato:>40s} {str(keyword_dato):>35s} {str(value_with_units):>48s}')

def imprimir_informacion():
        """
        Función que abre una imagen DICOM, extrae los datos detallados en private_tags.dat o cualquier archivo que contenga los tags y los imprime
        """
        print('Seleccione la operación')
        print('1. Visualizar Datos privados') 
        print('2. Visualizar Datos de CT') 
        print('3. Ingrese su propio archivo de tags')
        val = input("Ingrese selección: ")
        val = verificar.verificar(val)
        if val == 1:
                archivo = 'tags/private_tags.dat'
        elif val ==2:
                archivo = 'tags/CT_tags.dat'
        elif val == 3:
                archivo = str(input('Por favor ingrese la ruta del archivo con los tags: '))
        else:
                endex.endex()
        try:
                ruta = str(input('Por favor ingrese la ruta donde se encuentra la imagen: ')) 
                pydicom.dcmread(ruta)
                tags = np.loadtxt( archivo, delimiter= ',', dtype='str')
                headers = ('Tag', 'Name', 'Keyword', 'Value')
                print(f'{headers[0]:>12s}{headers[1]:>35s} {headers[2]:>35s} {headers[3]:>48s}')
                print('------------ ---------------------------------------- ----------------------------------- ------------------------------------------------')

                for tag in tags:
                   
                        try:    
                                tag_dato, name_dato,value_dato, keyword_dato, VR_dato, VM_dato= manejo_tags.return_data(ruta, tag[0], tag[1])  
                                if VR_dato == 'DA' and len(value_dato) != 0:
                                        value_with_units = str(datetime.strptime(value_dato, '%Y%m%d').strftime('%d/%m/%Y')) + tag[2]
                                        print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)
                                elif VR_dato == 'TM' and len(value_dato) != 0:
                                        if len(value_dato)==6:
                                                value_with_units = datetime.strptime(value_dato, '%H%M%S').strftime('%H:%M:%S')+ tag[2]
                                                print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)
                                        else:
                                                value_with_units = str(value_dato)+ tag[2]
                                                print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)
                                elif VR_dato == 'DS':
                                        value_with_units = str(value_dato)+ tag[2]
                                        print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)
                                elif VR_dato == 'IS':
                                        value_with_units = str(value_dato)+ tag[2]
                                        print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)
                                elif VR_dato == 'US':
                                        value_with_units = str(value_dato)+ tag[2]
                                        print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato) 
                                elif VR_dato == 'FD':
                                        value_with_units = str(value_dato)+ tag[2]
                                        print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)              
                                else:
                                        if len(str(value_dato)) != 0 :
                                                value_with_units = str(value_dato) + tag[2]
                                                print_data(tag_dato, name_dato,value_with_units, keyword_dato, VR_dato, VM_dato)
                        
                        except KeyError:
                                pass
        except:
                print("Archivo no encontrado!")         
