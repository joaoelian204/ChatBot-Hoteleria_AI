import os
import re

from config.settings import settings


def get_hotel_name():
    documentos_dir = settings.DOCUMENTOS_DIR
    posibles = []
    for fname in os.listdir(documentos_dir):
        if fname.endswith('.txt'):
            with open(os.path.join(documentos_dir, fname), encoding='utf-8') as f:
                for line in f:
                    if re.search(r'(hotel|hostal|resort|posada|inn)', line, re.IGNORECASE):
                        posibles.append(line.strip())
                        break
    if posibles:
        return posibles[0]
    # Si no encontró, intenta la primera línea del primer archivo
    for fname in os.listdir(documentos_dir):
        if fname.endswith('.txt'):
            with open(os.path.join(documentos_dir, fname), encoding='utf-8') as f:
                first = f.readline().strip()
                if first:
                    return first
    return None 