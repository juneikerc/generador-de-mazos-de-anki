#!/usr/bin/env python3
import json
import genanki
import random
import os

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
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div class="phrase">{{Phrase}}</div>',
            'afmt': '<div class="phrase">{{Phrase}}</div><hr><div class="translation">{{Translation}}</div>',
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

# Procesar las frases para resaltar las partes entre ****
def process_phrase(phrase):
    while '****' in phrase:
        start = phrase.find('****')
        end = phrase.find('****', start + 4)
        if start != -1 and end != -1:
            highlighted = phrase[start+4:end]
            phrase = phrase[:start] + '<span class="highlighted">' + highlighted + '</span>' + phrase[end+4:]
    return phrase

# Añadir las notas al mazo
for item in data:
    processed_phrase = process_phrase(item['phrase'])
    note = genanki.Note(
        model=model,
        fields=[processed_phrase, item['translation']]
    )
    deck.add_note(note)

# Crear el paquete de Anki
output_file = 'phrasal_verbs_deck.apkg'
genanki.Package(deck).write_to_file(output_file)

print(f"¡Mazo de Anki creado exitosamente! Archivo guardado como: {output_file}")
print(f"Total de tarjetas creadas: {len(data)}")
