#!/usr/bin/env python3
import json
import re

def count_characters_in_phrases(json_file):
    """
    Cuenta el total de caracteres en todas las frases en inglés del archivo JSON.
    Incluye todos los caracteres, incluyendo espacios y asteriscos.
    """
    try:
        # Cargar el archivo JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Contar caracteres en cada frase
        total_chars = 0
        total_chars_clean = 0  # Sin asteriscos
        
        for item in data:
            phrase = item.get('phrase', '')
            total_chars += len(phrase)
            
            # También contar caracteres sin los asteriscos (texto limpio)
            clean_phrase = re.sub(r'\*\*\*\*', '', phrase)
            total_chars_clean += len(clean_phrase)
        
        return {
            "total_phrases": len(data),
            "total_chars": total_chars,
            "total_chars_clean": total_chars_clean,
            "avg_chars_per_phrase": round(total_chars / len(data), 2) if data else 0
        }
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    json_file = "data.json"
    result = count_characters_in_phrases(json_file)
    
    print("\n=== ESTADÍSTICAS DE CARACTERES ===")
    print(f"Total de frases: {result['total_phrases']}")
    print(f"Total de caracteres (con asteriscos): {result['total_chars']}")
    print(f"Total de caracteres (sin asteriscos): {result['total_chars_clean']}")
    print(f"Promedio de caracteres por frase: {result['avg_chars_per_phrase']}")
    print("================================\n")
