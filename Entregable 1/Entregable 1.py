import requests

def validacion_dia ():
    while True:
        try:
            a = int(input("Ingrese el día: "))
            if isinstance(a, int):
                break
        except ValueError:
            print("Error, ingresa un valor numérico")       
    while a <= 0 or a >= 32:
        try:
            a = int(input("Ingresa un dato válido (01-31): "))
        except ValueError:
            print("Error, ingresa un valor numérico")
    a = str(a)
    if len(a) == 2:
        return str(a)
    else:
        return "0" + a

def validacion_mes ():
    while True:
        try:
            a = int(input("Ingrese el mes: "))
            if isinstance(a, int):
                break
        except ValueError:
            print("Error, ingresa un valor numérico")
    while a <= 0 or a >= 13:
        try:
            a = int(input("Ingresa un dato válido (01-12): "))
        except ValueError:
            print("Error, ingresa un valor numérico") 
    a = str(a)
    if len(a) == 2:
        return str(a)
    else:
        return "0" + a

def validacion_anio ():
    while True:
        try:
            a = int(input("Ingrese el año: "))
            if isinstance(a, int):
                break
        except ValueError:
            print("Error, ingresa un valor numérico")     
    while a <= 2000 or a >= 2025:
        try:
            a = int(input("Ingresa un dato válido (2001-2024): "))
        except ValueError:
            print("Error, ingresa un valor numérico")         
    return str(a)
    
    
        

#Función para consultar los asteroides cercanos en un rango de fechas
def obtener_asteroides(fecha_inicio, fecha_fin):
    #api_key = tAxP7VrtBVfd30iKCryvzM1N0biyGS8z8NjCsbqw
 #"DEMO_KEY"  #Obtener una personal en https://api.nasa.gov
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={fecha_inicio}&end_date={fecha_fin}&api_key=tAxP7VrtBVfd30iKCryvzM1N0biyGS8z8NjCsbqw"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        asteroides = []
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API. Verifica tu conexión.")
        exit()
    except requests.exceptions.Timeout:
        print("Error: La solicitud tardó demasiado en responder.")
        exit()
    for clave, lista in datos["near_earth_objects"].items():
        for asteroide in lista:
            nombre = list(asteroide["name"])
            #nombre1 = list(nombre)
            nombre.pop()
            nombre.pop(0)
            tamaño = asteroide["estimated_diameter"]["meters"]["estimated_diameter_max"]
            peligrosidad = asteroide["is_potentially_hazardous_asteroid"]
            for i in asteroide["close_approach_data"]:
                for clave, valor in i.items():
                    velocidad = i["relative_velocity"]["kilometers_per_hour"]
                    fecha = i["close_approach_date"]
                    for clave, valor in i["miss_distance"].items():
                        distancia = i["miss_distance"]["kilometers"]

            info = {
                "Fecha": fecha,
                "Nombre": "".join(nombre),
                "Es potencialmente peligroso": peligrosidad,
                "Tamaño (m)": round(tamaño, 2),
                "Velocidad (km/h)": round(float(velocidad), 2),
                "Distancia a la Tierra (km)": round(float(distancia), 2)
            }
            asteroides.append(info)
    return asteroides


#Solicitar las fechas
print("Las fechas deben de tener una diferencia de tiempo de máximo 7 dias y del año 2001 al 2024\n")
print("FECHA DE INICIO")
print("--------------------------------------")
dia = validacion_dia()
mes = validacion_mes()
anio = validacion_anio()
print("--------------------------------------\n")
print("FECHA DE FIN")
print("--------------------------------------")
dia_f = validacion_dia()
mes_f = validacion_mes()
anio_f = validacion_anio()
print("--------------------------------------\n")
fecha_inicio = f"{anio}-{mes}-{dia}"
fecha_fin = f"{anio_f}-{mes_f}-{dia_f}"

# Obtener y mostrar los asteroides
lista_asteroides = obtener_asteroides(fecha_inicio, fecha_fin)

# Mostrar datos
for a in lista_asteroides:
    for clave, valor in a.items():
        print(f"{clave}: {valor}")
    print("\n")
    
