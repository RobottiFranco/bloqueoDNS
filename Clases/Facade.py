import os

from .Consulta import *
from .ClienteAPI import *
from .CSVHandler import *
from .Grafico import *

def obtenerDatosOONI(limit, probe_cc, since, until, anomaly, ooni_run_link_id=None):
    url = Consulta(probe_cc, since, until, ooni_run_link_id)
    url = url.armar_consulta_db_OONI(limit, anomaly, "web_connectivity")
    print(url)
    
    datos = ClienteAPI(url, 3)
    datos = datos.realizar_solicitud_obtencion()
    if datos is None:
        print(f"No se pudieron obtener datos de {probe_cc}")
        return
    
    csv = CSVHandler()
    datosFiltrados = csv.filtrar_dns(datos)
    datos_sin_duplicados = csv.eliminar_duplicados(datosFiltrados)       
    
    if ooni_run_link_id is None:
        os.makedirs("Base_de_datos_OONI_por_ano", exist_ok=True)
        csv.guardar_en_csv(f"Base_de_datos_OONI_por_ano\\{probe_cc}.csv", datos_sin_duplicados, "a")
    else:
        os.makedirs("Base_de_datos_actualizada", exist_ok=True)
        csv.guardar_en_csv(f"Base_de_datos_actualizada\\{probe_cc}-{ooni_run_link_id}.csv", datos_sin_duplicados, "w")
        
        
def generar_graficos(probe_cc, since, until, time_grain, axis_x, test_name, ooni_run_link_id = None):
    print(f"Iniciando el proceso grafico de {probe_cc}...")
    
    url = Consulta(probe_cc, since, until, ooni_run_link_id)
    url = url.armar_consulta_grafica(time_grain, axis_x, test_name)
    
    datos = ClienteAPI(url, 3)
    datos = datos.realizar_solicitud_obtencion() 
       
    if datos is None:
        print(f"No se pudieron obtener datos de {probe_cc}")
        return
    
    grafico = Grafico(datos, probe_cc, ooni_run_link_id)
    grafico.graficarBarrasAnomalias()