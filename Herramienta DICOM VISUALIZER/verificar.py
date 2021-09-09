#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 29 18:41:27 2020

@author: Jennifer Ortega
"""
import endex

def verificar(x):
# Maneja errores, intenta un código y si sale error me llama a la
# función endex()
    try :
        eval(x)
        return eval(x)
    except:
        print('Elección no válida!')
        endex.endex()
