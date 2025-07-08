# Generador de Mazos de Anki - Phrasal Verbs

Este proyecto crea un mazo de Anki con tarjetas de estudio de phrasal verbs en inglés con sus traducciones al español, usando un diseño moderno y creativo.

## Requisitos

- Python 3.6 o superior
- Anki (para importar el mazo generado)

## Instalación

1. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

1. Asegúrate de que el archivo `data.json` esté en el mismo directorio que el script.
2. Ejecuta el script:

```bash
python create_anki_deck.py
```

3. Se generará un archivo `phrasal_verbs_deck.apkg` que puedes importar directamente en Anki.

## Características

- Diseño moderno con gradientes y efectos visuales
- Resaltado automático de los phrasal verbs en las frases
- Diseño responsivo que se adapta a diferentes tamaños de pantalla
- Estilo visual atractivo con tipografía clara

## Estructura de datos

El archivo `data.json` debe contener un array de objetos con la siguiente estructura:

```json
[
  {
    "phrase": "Texto en inglés con ****phrasal verb****",
    "translation": "Traducción al español"
  },
  ...
]
```

Los phrasal verbs deben estar rodeados por cuatro asteriscos (`****`) para que sean resaltados automáticamente en las tarjetas.

## Personalización

Puedes modificar el estilo CSS en el script `create_anki_deck.py` para cambiar la apariencia de las tarjetas según tus preferencias.
