import pandas as pd
import os

def analizar_datos():
    # Cargar el dataset (Asegúrate de que la carpeta y el archivo se llamen así)
    ruta_csv = 'data/sensores_industriales.csv'
    
    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_csv}'.")
        return

    print(" 1. Registros y Sensores Distintos")
    total_registros = len(df)
    sensores_distintos = df['id_sensor'].nunique()
    print(f"Total de registros: {total_registros}")
    print(f"Sensores distintos: {sensores_distintos}\n")

    print(" 2. Temperatura Promedio por Planta ")
    promedio_temp = df.groupby('planta')['temperatura_c'].mean()
    print(promedio_temp.to_string())
    print("\n")

    print(" 3. Temperatura Máxima (Sensor y Fecha) ")
    temp_maxima = df['temperatura_c'].max()
    registros_maximos = df[df['temperatura_c'] == temp_maxima][['id_sensor', 'fecha_hora', 'temperatura_c']]
    print(f"Temperatura máxima detectada: {temp_maxima}°C")
    print("Detalles:")
    print(registros_maximos.to_string(index=False))
    print("\n")

    print("4. Lecturas Mayores a 85 °C ")
    df_alertas = df[df['temperatura_c'] > 85]
    lecturas_peligro = len(df_alertas)
    print(f"Cantidad de lecturas > 85°C: {lecturas_peligro}\n")

    print("5. Planta con más alertas de temperatura ")
    conteo_alertas = df_alertas.groupby('planta').size()
    
    if not conteo_alertas.empty:
        max_alertas = conteo_alertas.max()
        plantas_top_alertas = conteo_alertas[conteo_alertas == max_alertas].index.tolist()
        print(f"Planta(s) con más alertas ({max_alertas} alertas): {', '.join(plantas_top_alertas)}\n")
    else:
        print("No se detectaron ninguna temperatura > 85°C).\n")

    print(" 6. Exportar resultados ")
    os.makedirs('resultados', exist_ok=True)
    ruta_salida = 'resultados/alertas.csv'
    
    df_alertas.to_csv(ruta_salida, index=False)
    print(f"Archivo exportado a: {ruta_salida}")

if __name__ == "__main__":
    analizar_datos()

