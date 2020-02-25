#©Copyright German Sanchez Lobo, febrero 2020, Panamá, ciudad de Panamá
#En mi edito de Visual Studio el programa ejecuta con py walletsyste.py, hay que colocar prefijo py
#Uso de funciones para el requirimiento de la asignación
#Se usan listas, arreglos, DataFrame de pandas.
#Se crea una base de datos inicial de nombre base05.csv
#La tasa de cambio se procesa y actualiza al principio de la aplicación para todas las monedas
#Los campos de la base de datos son: billetera, moneda, cantidad, saldo y fecha.
#Validaciones de monedas, si existen o no.
#Clave de billetera es 123, para todos los fines generales.
#La moneda puede ser introducida en minúscula o mayúscula
#Para la transferencia a otra billetera se valida si hay disponibilidad (moneda y cantidad)
#Al realizar las transferencia a otra billetara,la cantidad transferida queda en negativo

import requests #para uso de coinmarket
import numpy as np #arreglos para informes
import pandas as pd #estructura DataFrame para informes por moneda
import csv
import time
import operator
import os #verificar si el archivo para la base de datos está vacio

data_dict = {}
data_list = []
monedas=[]
cantidades=[]
cotizaciones=[]
data=[]
#Encabezado data csv
encab=['bille','crypto','qty','cash','date']

def dataempty():
    fstr = 'data05.csv'
    f = open('data05.csv', 'a') 
    w = csv.writer(f, delimiter = ',')
    if os.path.getsize(fstr) == 0:
        return(True)
    else:
        return(False)    

def esmoneda(cripto):
    criptos=["BTC","BCC","LTC","ETH","ETC","XRP"]
    cryptoaux = cripto.upper()
    return cryptoaux in criptos

def esnumero(numero):
    #return numero.replace('.',' ',1).isdigit() 
    return numero.isnumeric() 

def elsaldo(nbille, dolar): #en función a la cotizaciòn se calcula el saldo
    print("en el saldo")
    saldof=nbille*dolar
    return(saldof)

def mainmenu(): #menu de selección de opciones
    print()
    print("1.-Recibir cantidad")
    print("2.-Transferir monto")
    print("3.-Mostrar balance de una moneda")
    print("4.-Mostrar balance general")
    print("5.-Mostrar histórico de transacciones")
    print("6.-Salir")
    print()
    print("************************")
    opcion=input("Digite una opción: --> ")
    
    return(opcion)

def mainbody():    #funciòn para enviar a las funciones respectivas, de acuerdo a la opción
   
    iopcion = mainmenu()
    while not(iopcion.isnumeric()):
                print("Opción invalida")
                iopcion=input("Digite una opción: --> ")
    print()
    opcion = int(iopcion)
    while not((opcion>=1 and opcion <=6)):
        print("Opción invalida")
        opcion=int(input("Digite una opción: --> "))
    opcion = int(opcion)
    if opcion==1:
        recibircantidad()
    if opcion==2:
        transferirmonto()
    if opcion==3:
        mostrarbalancemoneda()
    if opcion==4:
        mostrarbalancegeneral()
    if opcion==5:
        historico()
    if opcion==6:
        exit()

def recibircantidad(): #función para ingresar crypto y cantidad , almacena en la BD data05.csv
    if dataempty()==True:
        w.writerow(['bille','cryp','qty','cash','date'])   
    i=0
    f = open('data05.csv', 'a') 
    print("\t.:MENU-1:.")
    while i<3:
         moneda = input("Ingrese el nombre de la moneda:->  ")
         while not esmoneda(moneda):
            print("Moneda invalida")
            moneda = input("Ingrese el nombre de la moneda:->  ")
         else:
            moneda = moneda.upper() 
            cantidad = int(input("Ingrese cantidad a comprar:->  "))
            data.append(moneda)
            data.append(cantidad)
            saldo = cantidad*data_dict[moneda]
            data.append(saldo)
            actualdate = time.strftime("%d/%m/%y")
            data.append(actualdate)
            w.writerow(data)
            f.flush()
            print("Operación exitosa con: ",moneda," con ", cantidad, " unidades")
            seguir = input("Desea cargar otra cryptomoneda (s/n)-> ")
            if (seguir =="n"):
                exit()
            else:
                data.clear()
                data.append(billetera)
                i+=1
                if i>2:
                    print("Maximo se puede cargar 3 cryptomonedas en cada intento")
                    exit()

def transferirmonto(): #Funciòn para transferir , verifica si hay condiciones para ello.
    if dataempty()==True:
        print("No existe data , debe realizar primero la opción 1")
        exit()
        #w.writerow(['bille','cryp','qty','cash','date'])   
    finalqty=0    
    datos=pd.read_csv('data05.csv', engine='python')
    df = pd.DataFrame(datos)
    isempty = df.empty
    if isempty==True:
        print("**Data de la billetera está vacia, por favor ir primero a la opción 1**")
        exit()
    ar=np.array(df)
    b2 = input("Indique billetera destino-> ")
    while not esnumero(b2):
        print("Error: Billetera debe ser numerica")
        b2 = input("Indique billetera destino-> ")
    b2=int(b2)    
    while(billetera==b2):
        print("Billeteras origen y final no pueden ser iguales")
        b2 = int(input("Indique billetera destino-> "))
    else:    
        continuar = True
        while continuar:
            moneda = input("Ingrese moneda a transferir:->  ")
            while not esmoneda(moneda):
                print("Moneda invalida")
                moneda = input("Ingrese el nombre de la moneda:->  ")
            else:
                moneda = moneda.upper() 
                cantidad = int(input("Ingrese cantidad a transferir:->  "))
                for i in range(len(ar)):
                    if ((ar[i][0]==billetera) & (ar[i][1]==moneda)):
                        finalqty = ar[i][2]+finalqty
                if ((finalqty ==0) or (finalqty<cantidad)) :
                    print("No dispone para realizar la transferencia")
                    exit()
                else:
                    data.append(moneda)
                    qtyaux=cantidad*(-1)
                    data.append(qtyaux)
                    saldo = (cantidad*data_dict[moneda])*(-1)
                    data.append(saldo)
                    actualdate = time.strftime("%d/%m/%y")
                    data.append(actualdate)
                    w.writerow(data)
                    print("Transferencia exitosa con: ",moneda," con ", cantidad, " unidades")
                    data.clear()
                    data.append(billetera)
                    continuar=False                              
    return()

def mostrarbalancemoneda(): #Solicita la moneda para calcular el balance total de ella
    if dataempty()==True:
        print("No existe data , debe realizar primero la opción 1")
        exit()
    datos=pd.read_csv('data05.csv')
    df = pd.DataFrame(datos)
    isempty = df.empty
    if isempty==True:
        print("**Data de la billetera está vacia, por favor ir primero a la opción 1**")
        exit()   
    ar=np.array(df)
    finalqty=0
    finalsaldo=0
    for i in range(len(ar)):
        if (ar[i][0]==billetera):
            finalqty = ar[i][2]+finalqty
    if finalqty==0:
        print("La billetera,  ", billetera, " no tiene transacciones")  
        exit() 
    finalqty=0
    moneda = input("Ingrese moneda para mostrar balance:->  ")
    while not esmoneda(moneda):
        print("Moneda invalida")
        moneda = input("Ingrese moneda para mostrar balance:->  ")
    else:
        moneda = moneda.upper() 
        for i in range(len(ar)):
            if ((ar[i][0]==billetera) & (ar[i][1]==moneda)):
                finalqty = ar[i][2]+finalqty
                finalsaldo = ar[i][3]+finalsaldo
        print("Balance por moneda:")
        print("************************")
        print("Moneda: ",moneda)
        print("Cantidad: ",finalqty)
        print('Saldo en $$: {:,.2f}'.format(finalsaldo))
        print("************************")
        print()
        seguir = input("Desea realizar otra opción (s/n)-> ")
        if (seguir =="s"):
            mainbody()
        else:
            exit()  
    return()

def mostrarbalancegeneral(): #Muestra el balance general, usando pandas
    if dataempty()==True:
        print("No existe data , debe realizar primero la opción 1")
        exit()
    datos=pd.read_csv('data05.csv')
    df = pd.DataFrame(datos)
    ar=np.array(df)
    isempty = df.empty
    finalqty=0
    if isempty==True:
        print("**Data de la billetera está vacia, por favor ir primero a la opción 1**")
        exit()
    for i in range(len(ar)):
        if (ar[i][0]==billetera):
            finalqty = ar[i][2]+finalqty
    if finalqty==0:
        print("La billetera,  ", billetera, " no tiene transacciones")  
        exit() 
    print("Balance general:")
    print("************************")
    print("Por Moneda: ")
    df1=df.groupby(['bille','cryp'])[['qty','cash']].sum()
    print(df1)
    print()
    print("Total $$ Billetera: ")
    df2=df.groupby(['bille'])[['cash']].sum()
    print(df2)
    print("************************")
    print()
    seguir = input("Desea realizar otra opción (s/n)-> ")
    if (seguir =="s"):
        mainbody()
    else:
        exit()  
    return()

def historico(): #Muestra histórico de transacciones , las negativas son transferencias a otras billeteras
    if dataempty()==True:
        print("No existe data , debe realizar primero la opción 1")
        exit()
    datos=pd.read_csv('data05.csv')
    df = pd.DataFrame(datos)
    isempty = df.empty
    if isempty==True:
        print("**Data de la billetera está vacia, por favor ir primero a la opción 1**")
        exit()
    ar=np.array(df)
    finalqty=0
    print("Historico de transacciones: ")
    for i in range(len(ar)):
        if (ar[i][0]==billetera):
            finalqty = ar[i][2]+finalqty
    if finalqty==0:
        print("La billetera,  ", billetera, " no tiene transacciones")  
        exit() 
    for i in range(len(ar)):
        dolaraux = ar[i][3]
        print("**********************************************************************************")
        print("Fecha: ",ar[i][4]," Billetera: ",ar[i][0], " Moneda: ",
        ar[i][1], "Cantidad ",ar[i][2]," $$: {:,.2f}".format(dolaraux))
        print("**********************************************************************************")
        print()
    seguir = input("Desea realizar otra opción (s/n)-> ")
    if (seguir =="s"):
        mainbody()
    else:
        exit()  
    return()

def tasadecambio(): #Sistema comienza con la actualización de las tasas de cambio
    criptosi=["BTC","LTC","ETH","ETC","XRP"]
    headers = {  'Accepts': 'application/json',  'X-CMC_PRO_API_KEY':  '0547cb93-7e9c-4535-b6af-03e3ade3637e'}
    for x in criptosi:
        print("Procesando actualización de tasas de cambio....")
        parametros = {'symbol': x}
        requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",headers=headers,params=parametros)
        data = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",headers=headers,params=parametros).json()
        y = (data["data"][x]["quote"]["USD"]["price"])
        data_dict[x]=y
    return()

#Main - aqui comienza el programa
fstr = 'data05.csv'
f = open('data05.csv', 'a')
w = csv.writer(f, delimiter = ',')
tasadecambio()
print()
print("SISTEMA CRIPTOMENDA")
print("************************")
print()
billetera = input("Ingrese el numero de la billetera:->  ")
while not esnumero(billetera):
    print("Error: Billetera debe ser numerica")
    billetera = input("Ingrese el numero de la billetera:->  ")
billetera = int(billetera)
data.append(billetera)
mainbody()
f.close