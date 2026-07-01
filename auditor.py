import os
import requests

def aplicar_cambio(archivo, tarea):
    prompt = f"Actúa como un experto en Python y seguridad. Aplica la siguiente mejora a este archivo: {tarea}. Devuélveme SOLO el código completo del archivo modificado sin explicaciones."
    # Aquí usaríamos la API de tu proxy que ya tienes corriendo en el puerto 8082
    print(f"Enviando solicitud para: {archivo}...")
    # (Lógica simplificada para llamar a tu DeepSeek)

# Ejecuta tu lista de 13 tareas aquí o pídeme a mí que te dé el código
