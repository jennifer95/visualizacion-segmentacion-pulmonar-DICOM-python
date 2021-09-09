#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 28 18:36:41 2020
Genera un menú
@author: nelson
"""
import verificar
import endex
import banner
import imprimir_informacion
import anonimizar
import imprimir_imagen as imp

def opciones():
    banner.print_banner()
    print('Seleccione la operación:')
    print('1. Vizualizar Datos en archivos DICOM') 
    print('2. Anonimización de Archivos DICOM') 
    print('3. Visualizar imágenes de archivos DICOM')
    print('4. Salir')
    val = input("Ingrese selección: ")
    val = verificar.verificar(val)
    if val == 1:
       imprimir_informacion.imprimir_informacion()       
    elif val == 2:
        print('Seleccione la operación')
        print('1. Anonimizar una imagen DICOM') 
        print('2. Anonimizar una carpeta de un paciente') 
        print('3. Anonimizar carpetas con varios pacientes') 
        val = input("Ingrese selección: ")
        val = verificar.verificar(val)
        if val == 1:
            anonimizar.anonimizar_img()
        elif val == 2:
            anonimizar.anonimizar_paciente()
        elif val == 3:
            anonimizar.anonimizar_carpeta()
    elif val == 3:
        print('Seleccione la operación:')
        print('1. Visualizar una imagen DICOM') 
        print('2. Visualizar un examen completo de CT') 
        val = input("Ingrese selección: ")
        val = verificar.verificar(val)
        if val == 1:
            try:
                imp.visualizar_pantalla()
            except:
                print('Archivo no encontrado') 
        elif val == 2:
            print('Visuaización Estilo iQ-LITE 3.0.0.')
            print('1. Visualización axial') 
            print('2. Visualización coronal') 
            print('3. Visualización sagital')
            val = input("Ingrese selección: ")
            val = verificar.verificar(val)
            if val == 1:
                tipo_plano = 'axial'
                try: 
                        imp.visualizar_pantalla_mult(tipo_plano)
                except:
                    print('Error al ingresar los parámetros') 
            elif val == 2:
                try:
                        tipo_plano = 'coronal'
                        imp.visualizar_pantalla_mult(tipo_plano)
                except:
                        print('Error al ingresar los parámetros')
            elif val == 3:
                tipo_plano = 'sagital'
                try:
                        imp.visualizar_pantalla_mult(tipo_plano)
                except:
                        print('Error al ingresar los parámetros')
    else:
        endex.endex()






