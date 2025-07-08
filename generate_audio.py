#!/usr/bin/env python3
import json
import os
import time
import hashlib
import base64
import re
from dotenv import load_dotenv
from tqdm import tqdm

# Para ElevenLabs
from elevenlabs import generate, set_api_key

# Para Hume.ai
from hume import HumeVoiceClient

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
HUMEAI_API_KEY = os.getenv("HUMEAI_API_KEY")
AUDIO_PROVIDER = "elevenlabs"  # Opciones: "elevenlabs" o "humeai"
SOUNDS_DIR = "sounds"
DATA_FILE = "data.json"

# Configurar ElevenLabs API key
if ELEVENLABS_API_KEY:
    set_api_key(ELEVENLABS_API_KEY)

# Inicializar el cliente de Hume.ai si la API key está disponible
hume_client = None
if HUMEAI_API_KEY:
    hume_client = HumeVoiceClient(api_key=HUMEAI_API_KEY)

# Asegurarse de que el directorio de sonidos exista
if not os.path.exists(SOUNDS_DIR):
    os.makedirs(SOUNDS_DIR)

def clean_text_for_filename(text):
    """Limpia el texto para usarlo como nombre de archivo"""
    # Eliminar los asteriscos que rodean las palabras destacadas
    text = re.sub(r'\*\*\*\*(.*?)\*\*\*\*', r'\1', text)
    # Eliminar caracteres no permitidos en nombres de archivo
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    # Limitar la longitud del nombre del archivo
    if len(text) > 100:
        text = text[:97] + "..."
    return text

def get_audio_filename(phrase):
    """Genera un nombre de archivo único basado en el contenido de la frase"""
    # Crear un hash del texto para asegurar nombres únicos
    phrase_hash = hashlib.md5(phrase.encode()).hexdigest()[:8]
    # Limpiar el texto para el nombre del archivo
    clean_phrase = clean_text_for_filename(phrase)
    return f"{clean_phrase}_{phrase_hash}.mp3"

def generate_audio_elevenlabs(text, output_file):
    """Genera audio usando la API de ElevenLabs"""
    try:
        # Generar audio usando el SDK de ElevenLabs
        audio = generate(
            text=text,
            voice="21m00Tcm4TlvDq8ikWAM",  # Puedes cambiar a otras voces disponibles
            model="eleven_multilingual_v2"
        )
        
        # Guardar el audio en un archivo
        with open(output_file, "wb") as f:
            f.write(audio)
        
        print(f"Audio generado correctamente con ElevenLabs: {output_file}")
        return True
    except Exception as e:
        print(f"Error al generar audio con ElevenLabs: {str(e)}")
        return False

def generate_audio_humeai(text, output_file):
    """Genera audio usando el SDK de Hume.ai"""
    try:
        if hume_client is None:
            print("Error: Cliente de Hume.ai no inicializado. Verifica tu API key.")
            return False
        
        # Generar audio usando el SDK de Hume.ai
        # La API actual de Hume.ai puede ser diferente, esta es una implementación básica
        # basada en la documentación actual
        audio_bytes = hume_client.synthesize_speech(
            text=text,
            voice_id="female_a"  # Usar una voz predeterminada, ajustar según disponibilidad
        )
        
        # Guardar el audio en un archivo
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
        
        print(f"Audio generado correctamente con Hume.ai: {output_file}")
        return True
    except Exception as e:
        print(f"Error al generar audio con Hume.ai: {str(e)}")
        return False

def generate_audio(text, output_file, provider):
    """Genera audio usando el proveedor especificado"""
    if provider == "elevenlabs":
        return generate_audio_elevenlabs(text, output_file)
    elif provider == "humeai":
        return generate_audio_humeai(text, output_file)
    else:
        print(f"Proveedor no válido: {provider}")
        return False

def process_phrases(data, audio_provider):
    """Procesa todas las frases y genera audio para cada una"""
    # Verificar si las claves API están configuradas
    if audio_provider == "elevenlabs" and not ELEVENLABS_API_KEY:
        print("Error: La clave API de ElevenLabs no está configurada. Por favor, configúrela en el archivo .env")
        return
    
    if audio_provider == "humeai" and not HUMEAI_API_KEY:
        print("Error: La clave API de Hume.ai no está configurada. Por favor, configúrela en el archivo .env")
        return
    
    # Variable para alternar entre proveedores si se desea
    current_provider = audio_provider
    
    # Generar audio para cada frase
    for i, item in enumerate(tqdm(data, desc="Generando audio")):
        phrase = item["phrase"]
        
        # Limpiar la frase para la generación de audio (quitar los asteriscos)
        clean_phrase = re.sub(r'\*\*\*\*(.*?)\*\*\*\*', r'\1', phrase)
        
        # Generar nombre de archivo
        audio_filename = get_audio_filename(phrase)
        audio_path = os.path.join(SOUNDS_DIR, audio_filename)
        
        # Verificar si el archivo ya existe
        if os.path.exists(audio_path):
            print(f"El archivo {audio_filename} ya existe. Omitiendo...")
            continue
        
        # Generar audio
        success = generate_audio(clean_phrase, audio_path, current_provider)
        
        # Alternar entre proveedores si se desea
        # Descomenta la siguiente línea para alternar automáticamente
        # current_provider = "humeai" if current_provider == "elevenlabs" else "elevenlabs"
        
        # Esperar un poco para no sobrecargar la API
        if success and i < len(data) - 1:
            time.sleep(1)

def main():
    # Cargar los datos del archivo JSON
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error al cargar el archivo de datos: {str(e)}")
        return
    
    print(f"Cargados {len(data)} elementos del archivo JSON")
    print(f"Proveedor de audio seleccionado: {AUDIO_PROVIDER}")
    
    process_phrases(data, AUDIO_PROVIDER)

if __name__ == "__main__":
    main()
