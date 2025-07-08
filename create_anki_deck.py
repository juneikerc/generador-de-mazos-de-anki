#!/usr/bin/env python3
import json
import genanki
import random
import os
import re
import hashlib

# Cargar los datos del archivo JSON
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Crear un ID de modelo aleatorio (necesario para genanki)
model_id = random.randrange(1 << 30, 1 << 31)

# Definir el estilo CSS moderno y creativo para las tarjetas
css = '''
.card {
    font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    color: #333;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.phrase {
    font-size: 24px;
    font-weight: 500;
    line-height: 1.4;
    margin-bottom: 20px;
    color: #2c3e50;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 10px;
    position: relative;
}

.phrase::before {
    content: """;
    font-size: 60px;
    color: #3498db;
    position: absolute;
    top: -20px;
    left: 5px;
    opacity: 0.3;
}

.phrase::after {
    content: """;
    font-size: 60px;
    color: #3498db;
    position: absolute;
    bottom: -50px;
    right: 5px;
    opacity: 0.3;
}

.translation {
    font-size: 22px;
    font-weight: 400;
    color: #16a085;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    border-left: 4px solid #16a085;
    text-align: left;
    margin-top: 30px;
}

.highlighted {
    color: #e74c3c;
    font-weight: bold;
    background-color: rgba(231, 76, 60, 0.1);
    padding: 0 5px;
    border-radius: 3px;
}

@media (max-width: 480px) {
    .phrase {
        font-size: 20px;
    }
    .translation {
        font-size: 18px;
    }
}
'''

# Definir el modelo de la tarjeta
model = genanki.Model(
    model_id,
    'Phrasal Verbs Model',
    fields=[
        {'name': 'Phrase'},
        {'name': 'Translation'},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Audio}}<div class="phrase">{{Phrase}}</div>',
            'afmt': '{{Audio}}<div class="phrase">{{Phrase}}</div><hr><div class="translation">{{Translation}}</div>',
        },
    ],
    css=css,
)

# Crear un ID de mazo aleatorio
deck_id = random.randrange(1 << 30, 1 << 31)

# Crear el mazo
deck = genanki.Deck(
    deck_id,
    'Phrasal Verbs - Español/Inglés'
)

# Función para generar el nombre del archivo de audio (igual que en generate_audio.py)
def get_audio_filename(text):
    """Genera un nombre de archivo basado en el texto y un hash"""
    # Limpiar el texto para usarlo como nombre de archivo
    clean_text = re.sub(r'\*\*\*\*(.*?)\*\*\*\*', r'\1', text)
    # Eliminar caracteres no permitidos en nombres de archivo
    clean_text = re.sub(r'[\\/*?:"<>|]', "", clean_text)
    # Limitar la longitud del nombre del archivo
    if len(clean_text) > 100:
        clean_text = clean_text[:100]
    
    # Generar un hash único para evitar colisiones
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    
    # Crear el nombre del archivo
    filename = f"{clean_text}_{text_hash}.mp3"
    return filename

# Procesar las frases para resaltar las partes entre ****
def process_phrase(phrase):
    while '****' in phrase:
        start = phrase.find('****')
        end = phrase.find('****', start + 4)
        if start != -1 and end != -1:
            highlighted = phrase[start+4:end]
            phrase = phrase[:start] + '<span class="highlighted">' + highlighted + '</span>' + phrase[end+4:]
    return phrase

# Directorio donde se encuentran los archivos de audio
SOUNDS_DIR = "sounds"

# Verificar que el directorio de sonidos exista
if not os.path.exists(SOUNDS_DIR):
    print(f"Advertencia: El directorio {SOUNDS_DIR} no existe. No se incluirán archivos de audio.")

# Crear una lista para almacenar los archivos de medios
media_files = []

# Añadir las notas al mazo
for item in data:
    phrase = item['phrase']
    processed_phrase = process_phrase(phrase)
    
    # Generar el nombre del archivo de audio
    audio_filename = get_audio_filename(phrase)
    audio_path = os.path.join(SOUNDS_DIR, audio_filename)
    
    # Verificar si el archivo de audio existe
    audio_tag = ""
    if os.path.exists(audio_path):
        audio_tag = f"[sound:{audio_filename}]"
        media_files.append(audio_path)
    else:
        print(f"Advertencia: No se encontró el archivo de audio para: {phrase}")
    
    note = genanki.Note(
        model=model,
        fields=[processed_phrase, item['translation'], audio_tag]
    )
    deck.add_note(note)

# Crear el paquete de Anki con los archivos de medios
output_file = 'phrasal_verbs_deck.apkg'
genanki.Package(deck, media_files=media_files).write_to_file(output_file)

print(f"¡Mazo de Anki creado exitosamente! Archivo guardado como: {output_file}")
print(f"Total de tarjetas creadas: {len(data)}")
