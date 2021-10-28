# -*- coding: utf-8 -*-

# Carga librerías
import bs4 as bs
import pandas as pd
import requests
import schedule
import time

# Crea un dataframe vacío
cols = ["fecha", "temp", "hum", "p_rocio", "pres_bar", "viento", "lluvia", "r_solar", "r_uv"] 
df = pd.DataFrame(columns = cols)
# Guarda el df en un archivo CSV
datos = df.to_csv("datos_ema_unsam.csv", index = False)

def ema_unsam():
    
    # Lee el archivo CSV creado anteriormente
    df = pd.read_csv("datos_ema_unsam.csv")
    
    # Descarga el código HTML
    url = requests.get("https://ema.unsam.edu.ar/")
    soup = bs.BeautifulSoup(url.content, "html.parser")
    
    # Extrae el contenido de las etiquetas donde se encuentra la fecha y hora
    tags_font = soup.find_all("font", {"size":"3"})
    # Crea una lista con el contenido de la etiqueta font
    datos_font = [tag.text for tag in tags_font]
    # Extrae solo los datos de fecha y hora
    fecha = " ".join(datos_font[0:2])
    
    # Extrae el contenido de las etiquetas donde se encuentra la información meteorológica
    tags_p = soup.find_all("p", {"align":"center"})
    # Crea una lista con el contenido de la etiqueta p
    datos_p = [tag.text for tag in tags_p]
    # Extrae los datos meteorológicos. Solo los valores numéricos
    temp = datos_p[1].split(" ")[0]
    hum = datos_p[6].split(" ")[0]
    rocio = datos_p[11].split(" ")[0]
    presion = datos_p[21].split(" ")[0]
    viento = datos_p[24].split(" ")[0]
    lluvia = datos_p[31].split(" ")[0]
    r_solar = datos_p[37].split(" ")[0]
    r_uv = datos_p[40].split(" ")[0]
    
    # Crea una lista con todos los datos
    datos = [fecha, temp, hum, rocio, presion, viento, lluvia, r_solar, r_uv]
    
    # Agrega los datos al df en una nueva fila
    nueva_fila = pd.Series(datos, index = df.columns)
    df = df.append(nueva_fila, ignore_index = True)
    # Exporta los datos al CSV
    df.to_csv("datos_ema_unsam.csv", index = False)

# Crea una rutina para llamar a la función ema_unsam() cada una hora       
schedule.every().hour.do(ema_unsam).run()

while True:
    schedule.run_pending()
    time.sleep(1)  
