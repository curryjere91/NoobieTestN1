#!/usr/bin/env python3
# -*-coding: utf-8 -*-
import tkinter as tk
import pymysql
from tkinter import *
import os
import subprocess
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import ttk

Ntarjeta=""
Dni=""
Comercio=""
Nterminal=""
Distribuidor=""
Producto=""
Fecha=""
Hora=""
Modo=""
Nrcomercio=""

def Conexion_distribuidor(Nro_terminal):
    conexion = pymysql.connect(host="localhost",
                               user="Suzaku",
                               passwd="suzaku496",
                               database="Terminales_soli")
    cursor = conexion.cursor()
    registros = "select * from Terminales where Nro_terminal='" + str(Nro_terminal) + "';"
    # Mostrar registros
    cursor.execute(registros)
    filas = cursor.fetchall()

    global Nterminal
    global Comercio
    global Distribuidor
    global Nrcomercio
    for fila in filas:
        Nterminal = fila[1]
        Comercio = fila[2]
        Distribuidor = fila[3]
        Nrcomercio = fila[4]
        if(Distribuidor == "SG"):
            Distribuidor = "SG                 "
        if(Distribuidor == "Distrigas"):
            Distribuidor = "Distrigas          "


    conexion.commit()
    conexion.close()

def sgas_usuario(Busqueda):
    conexion = pymysql.connect(host="192.168.100.6",
                               user="dbadmin",
                               passwd="qz$mp0-",
                               database="kigsolidario2")
    cursor = conexion.cursor()
    registros = "select * from sgas_usuario where nro_doc='" + str(Busqueda) + "' OR nro_tarjeta='" + str(
        Busqueda) + "';"
    cursor.execute(registros)
    filas = cursor.fetchall()
    global NumTarMy
    for fila in filas:
        NomUsuMy = fila[10]
        NumCueMy = fila[2]
        SituacMy = fila[6]
        NumTarMy = fila[0]
        NumDocMy = fila[21]
        FecVtoMy = fila[25]
        DomiciMy = fila[13]
        LocaliMy = fila[15]
        NumCvvMy = fila[32]
    iso_pool(NumTarMy, Fecha_desde, Fecha_Hasta)
    conexion.commit()
    conexion.close()

def iso_pool(Nro_Tarjeta, Fecha_desde, Fecha_Hasta):
    conexion = pymysql.connect(host="192.168.100.6",
                               user="dbadmin",
                               passwd="qz$mp0-",
                               database="kigsolidario2")
    cursor = conexion.cursor()
    registros = "SELECT * FROM iso_pool WHERE mtype ='0200' and retrefnum_37 > 0 and datetime_trx >'" + str(Fecha_desde) +"'AND datetime_trx <'"+ str(Fecha_Hasta) +" 23:59:59' and (track2_35 like '" + str(Nro_Tarjeta) + "%' or pan_2 like '" + str(Nro_Tarjeta) + "') order by datetime_trx DESC;"
    cursor.execute(registros)
    filas = cursor.fetchall()
    print (" ")
    print(
        "+----CONSULTA SOLIDARIDAD------------------------------------------------------------------------------------------------------------------+")
    print('{8}{0:18s}{8} {1:21s}{8} {2:18s}{8} {3:11s}{8} {4:10s}{8} {5:14s}{8} {6:24s}{8} {7:8s}{8}'.format("Numero de Tarjeta",
                                                                                                  "Fecha y Hora",
                                                                                                  "Producto",
                                                                                                  "Comprobante",
                                                                                                  "DNI",
                                                                                                  "Nro Terminal",
                                                                                                  "Distribuidor",
                                                                                                  "Modo", "|"))
    print(
        "+------------------+----------------------+-------------------+------------+-----------+---------------+-------------------------+---------+")

    for fila in filas:
        pan2 = fila[3]
        mtype = fila[1]
        datetime = fila[35]
        Nro_terminal = fila[20]
        track2_35 = fila[16]
        Producto = fila [25]
        Nro_comer =fila [21]
        NComprobante = fila[31]
        Nprod=""
        if Producto == "993":
            Nprod = "Garrafa 10Kg"
        if Producto == "994":
            Nprod = "Garrafa 15Kg"
        if Producto == "995":
            Nprod = "Garrafa 30Kg"
        if Producto == "996":
            Nprod = "Tubo 45Kg   "
        if Producto == "997":
            Nprod = "Kilo Gas    "

        if bool(pan2):
            Modo="Manual"
        else:
            Modo="Banda"
        Nproducto= str(Producto) + " " + str(Nprod)

        Nro_terminal="60" + str(Nro_terminal[2:8])
        Conexion_distribuidor(Nro_terminal)
        print('{8}{0:18s}{8} {1:21s}{8} {2:18s}{8} {3:11s}{8} {4:10s}{8} {5:14s}{8} {6:24s}{8} {7:8s}{8}'.format(NumTarMy, str(datetime), Nproducto,NComprobante , DNIbus, Nro_terminal, Distribuidor, Modo, "|"))
    print("+------------------+----------------------+-------------------+------------+-----------+---------------+-------------------------+---------+")

    conexion.commit()
    conexion.close()

print("Ingrese DNI: ", end="")
DNIbus=input()
print("Ingrese Fecha Desde:(DDMMAAAA) ", end="")
Fecha_desde=input()
Fecha_desde=str(Fecha_desde[4:8]) + "-" + str(Fecha_desde[2:4] + "-" + str(Fecha_desde[0:2]))
print("Ingrese Fecha Hasta:(DDMMAAAA) ", end="")
Fecha_Hasta=input()
Fecha_Hasta=str(Fecha_Hasta[4:8]) + "-" + str(Fecha_Hasta[2:4] + "-" + str(Fecha_Hasta[0:2]))

#DNIbus="16412602"
#Fecha_desde="2021-11-03"
#Fecha_Hasta="2021-11-29"

sgas_usuario(DNIbus)
