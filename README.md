# Generador de Mazos de Anki con Audio TTS inglés/español

Este proyecto es una suite de herramientas en Python para crear mazos de Anki personalizados para el aprendizaje de idiomas, con un enfoque en la generación de audio a través de servicios de Texto a Voz (TTS).

Con estos scripts, puedes convertir una lista de frases en un archivo JSON en un mazo de Anki profesional, con audio de alta calidad para cada tarjeta, un diseño moderno y la capacidad de personalizar el contenido y la apariencia.

---

**¿Necesitas un mazo de Anki personalizado?**

Si quieres un mazo de Anki hecho a medida sobre cualquier tema (idiomas, ciencias, historia, etc.), no dudes en contactarme. Visita [juneikerc.com](https://juneikerc.com) para más información.

---

## ✨ Características

- **Creación de Mazos de Anki**: Genera archivos `.apkg` listos para importar en Anki.
- **Integración de Audio TTS**: Soporta múltiples proveedores de TTS para generar audio automáticamente:
  - **ElevenLabs**: Voces de alta calidad y realismo.
  - **Replicate (Chatterbox)**: Una alternativa de código abierto.
- **Diseño de Tarjetas Moderno**: Las tarjetas tienen un estilo CSS moderno, limpio y responsivo.
- **Personalización**:
  - Nombres de mazo y archivos de salida personalizables a través de la línea de comandos.
  - Resaltado automático de palabras clave en las tarjetas (usando \*\*\*\*).
- **Estimación de Costos**: Incluye un script para contar caracteres y estimar el uso de las APIs de TTS.
- **Eficiencia**: Evita generar archivos de audio que ya existen, ahorrando tiempo y costos de API.

## Workflow del Proyecto

El proceso para crear un mazo de Anki con audio se divide en tres pasos principales:

1.  **`count_characters.py` (Opcional)**: Analiza tu archivo de datos para darte un recuento total de caracteres. Esto es útil para estimar cuánto podrías gastar en las APIs de TTS antes de generar los audios.

2.  **`generate_audio.py`**: Lee el archivo `data.json` y genera un archivo de audio `.mp3` para cada frase utilizando el proveedor de TTS que elijas (ElevenLabs o Replicate).

3.  **`create_anki_deck.py`**: Crea el mazo de Anki (`.apkg`). Este script toma las frases del archivo `data.json`, las formatea y adjunta los archivos de audio generados en el paso anterior.

---

## 🚀 Guía de Inicio Rápido

Sigue estos pasos para poner en marcha el proyecto.

### 1. Prerrequisitos

- Python 3.7 o superior
- Una cuenta en [ElevenLabs](https://elevenlabs.io/) o [Replicate](https://replicate.com/) para obtener tus claves de API.

### 2. Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/juneikerc/generador-de-mazos-de-anki.git
cd generador-de-mazos-de-anki

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt
```

### 3. Configuración

Antes de ejecutar los scripts, necesitas configurar tus claves de API.

```bash
# 1. Copia el archivo de ejemplo .env.example a .env
cp .env.example .env
```

2.  Crea el archivo `.env` y añade tus claves de API:

```dotenv
# Claves API para los servicios de generación de voz
ELEVENLABS_API_KEY=tu_clave_de_elevenlabs
REPLICATE_API_TOKEN=tu_token_de_replicate
```

### 4. Preparar los Datos

El script utiliza un archivo `data.json` para obtener las frases. El formato debe ser un array de objetos JSON:

```json
[
  {
    "phrase": "She decided to ****call off**** the meeting.",
    "translation": "Ella decidió cancelar la reunión."
  },
  {
    "phrase": "He needs to ****look after**** his younger brother.",
    "translation": "Él necesita cuidar a su hermano menor."
  }
]
```

- `phrase`: La frase en inglés. Usa `****` para resaltar el phrasal verb que se mostrará con un estilo diferente en la tarjeta.
- `translation`: La traducción al español.

### 5. Ejecutar los Scripts

Ahora estás listo para generar tu mazo.

**Paso 1: Generar los Audios**

Ejecuta el script `generate_audio.py`. Puedes elegir el proveedor de audio editando el script y cambiando la variable `AUDIO_PROVIDER` a `"elevenlabs"` o `"replicate"`.

```bash
python generate_audio.py
```

Los archivos de audio se guardarán en la carpeta `sounds/`.

**Paso 2: Crear el Mazo de Anki**

Una vez que los audios estén generados, crea el mazo.

```bash
# Crear un mazo con un nombre personalizado
python create_anki_deck.py -n "Mi Mazo de Phrasal Verbs"

# El nombre del archivo de salida se generará automáticamente (ej: Mi_Mazo_de_Phrasal_Verbs.apkg)
```

¡Y listo! Ahora puedes importar el archivo `.apkg` generado en tu aplicación de Anki.

## ⚙️ Uso Avanzado de Scripts

### `create_anki_deck.py`

Puedes personalizar la creación del mazo con los siguientes argumentos:

- `-n`, `--name`: Define el nombre del mazo.
- `-o`, `--output`: Especifica el nombre del archivo de salida. Si no se usa, se genera a partir del nombre del mazo.
- `-d`, `--data`: Ruta al archivo JSON de datos.
- `-s`, `--sounds-dir`: Directorio donde se encuentran los audios.

```bash
# Ejemplo con más personalización
python create_anki_deck.py --name "Inglés Avanzado S1" --output "ingles_s1.apkg"
```

### `count_characters.py`

Para saber cuántos caracteres se enviarán a la API de TTS, usa este script:

```bash
python count_characters.py
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

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
