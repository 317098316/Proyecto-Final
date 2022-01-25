# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 10:09:23 2022

@author: DIEGO
"""
import pandas as pd
import pandasql as ps
#from urllib.request import urlopen
#import urllib.request
#import requests
import time 
import numpy as np
import re
from selenium import webdriver
aux=pd.DataFrame()
aux.to_excel("df_guadalajara.xlsx",index=False)

def Buscador_Precios_FGuadalajara(producto,mypath):
    
    path = mypath
    driver=webdriver.Chrome(path)
    url= "https://www.farmaciasguadalajara.com/SearchDisplay?categoryId=&storeId=10151&searchType=1001&catalogId=10052&langId=-24&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&pageSize=20&searchTerm="+producto
    driver.get(url)
        
    productos= driver.find_elements_by_class_name("product_info")
    ### accedemos a las urls almacenadas en la variable productos

    lista_urls=list()
    for i in range(len(productos)):
        try:
            lista_urls.append(productos[i].find_element_by_tag_name("a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)
            
    ### accedemos a los nombres de los productos

    lista_nombres=list()

    for i in range(len(productos)):
        try:
            lista_nombres.append(productos[i].find_elements_by_tag_name("a")[0].text)
        except:
            lista_nombres.append(np.nan)
        
    lista_precios1=list()

    for i in range(len(productos)):
        try:
            lista_precios1.append(productos[i].find_elements_by_class_name("product_price")[0].text.split("\n"))
        except:
            lista_precios1.append(np.nan)

    lista_precios=list()
    lista_promos=list()

    for i in range(len(productos)):
        try:
            lista_precios.append(lista_precios1[i][0])
        except:
            lista_precios.append(np.nan)

    for i in range(len(productos)):
        try:
            lista_promos.append(lista_precios1[i][1])
        except:
            lista_promos.append(np.nan)

    df_guadalajara = pd.DataFrame({"Nombre":lista_nombres,"URL":lista_urls,"Precio":lista_precios,"Precio con descuento":lista_promos})
    df_guadalajara["Farmacia"]="Guadalajara"
    df_guadalajara["Medicamento"]= producto
    df_guadalajara["Fecha"]= time.strftime("%d/%m/%y")
    df_guadalajara = df_guadalajara[["Fecha","Farmacia","Medicamento","Nombre","URL","Precio","Precio con descuento"]]

    datos_webscraper=pd.read_excel("df_guadalajara.xlsx")
    datos_webscraper= pd.concat([datos_webscraper,df_guadalajara],axis=0)
    datos_webscraper.to_excel("df_guadalajara.xlsx",index=False)
    driver.quit()
    
    return df_guadalajara


def Precios(path):
    for productos in ["Ibuprofeno 400mg","Paracetamol 500mg","Clonazepam 2mg","Viagra 100mg"]:
        Buscador_Precios_FGuadalajara(productos,path)

Precios("C:\WebDriver\chromedriver.exe")
