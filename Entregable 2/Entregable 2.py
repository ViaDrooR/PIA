import requests
import re

#Validaciones de fecha
def validacion_dia ():
    patron = r"\b(0?[1-9]|[12][0-9]|3[01])\b"
    compilacion = re.compile(patron)
    while True:
        a = input("Ingrese el día [01-31]: ")
        mo = compilacion.search(a)
        if mo:
            a = int(mo.group())           
            break
        else:
            print("Error, valor no válido. Intente de nuevo")
    a = str(a)
    if len(a) == 2:
        return str(a)
    else:
        return "0" + a

def validacion_mes ():
    patron = r"\b(0?[1-9]|1[0-2])\b"
    compilacion = re.compile(patron)
    while True:
        a = input("Ingrese el mes [01-12]: ")
        mo = compilacion.search(a)
        if mo:
            a = int(mo.group())           
            break
        else:
            print("Error, valor no válido. Intente de nuevo")
    a = str(a)
    if len(a) == 2:
        return str(a)
    else:
        return "0" + a

def validacion_anio ():
    patron = r"\b(200[1-9]|201[0-9]|202[0-5])\b"
    compilacion = re.compile(patron)
    while True:
        a = input("Ingrese el año [2001-2025]: ")
        mo = compilacion.search(a)
        if mo:
            a = int(mo.group())
            break
        else:
            print("Error, valor no válido. Intente de nuevo")
    return str(a)

#Función para consultar los asteroides cercanos en un rango de fechas
def obtener_asteroides(fecha_inicio, fecha_fin):
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
    except Exception:
        print("Error. Intente de Nuevo")
        exit()
    for fecha in sorted(datos["near_earth_objects"].keys()):
        lista = datos["near_earth_objects"][fecha]
        for asteroide in lista:
            nombre = list(asteroide["name"])
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
                "Es peligroso": str(peligrosidad),
                "Tamaño (m)": round(float(tamaño), 2),
                "Velocidad (km/h)": round(float(velocidad), 2),
                "Distancia a la Tierra (km)": round(float(distancia), 2)
            }
            asteroides.append(info)
    return asteroides



#Solicitar las fechas
print("Las fechas deben de tener una diferencia de máximo 7 días y del año 2001 al 2024\n")

print("FECHA DE INICIO")
print("--------------------------------------")
dia = validacion_dia()
mes = validacion_mes()
anio = validacion_anio()
print("--------------------------------------")

print("FECHA DE FIN")
print("--------------------------------------")
dia_f = validacion_dia()
mes_f = validacion_mes()
anio_f = validacion_anio()
print("--------------------------------------")

fecha_inicio = f"{anio}-{mes}-{dia}"
fecha_fin = f"{anio_f}-{mes_f}-{dia_f}"

# Obtener y mostrar los asteroides
lista_asteroides = obtener_asteroides(fecha_inicio, fecha_fin)

# Mostrar datos
for a in lista_asteroides:
    for clave, valor in a.items():
        print(f"{clave}: {valor}")
    print("\n")

#Guardar en .txt
if lista_asteroides:
    with open("asteroides_2024.txt", "a", encoding="utf-8") as archivo_txt:
        for asteroide in lista_asteroides:
            for clave, valor in asteroide.items():
                archivo_txt.write(f"{clave}: {valor}\n")
            archivo_txt.write("\n")
