#!/usr/bin/env python
"""
Script para corregir las rutas en todas las páginas HTML
"""
import os
import re
from pathlib import Path

# Directorio de templates
TEMPLATES_DIR = Path('sigelin/templates/frontend')

# Archivos a corregir
FILES = [
    'Equipos.html',
    'Reparaciones.html',
    'Inventario.html',
    'Reportes.html'
]

# Patrones a reemplazar
REPLACEMENTS = [
    (r'href="dashboard\.html"', 'href="/dashboard.html"'),
    (r'href="equipos\.html"', 'href="/equipos.html"'),
    (r'href="reparaciones\.html"', 'href="/reparaciones.html"'),
    (r'href="inventario\.html"', 'href="/inventario.html"'),
    (r'href="reportes\.html"', 'href="/reportes.html"'),
    (r'href="index\.html"', 'href="/"'),
    (r'window\.location\.href = "index\.html"', 'window.location.href = "/"'),
    (r'window\.location\.href = "dashboard\.html"', 'window.location.href = "/dashboard.html"'),
]

def fix_file(filepath):
    """Corregir un archivo HTML"""
    print(f"Corrigiendo: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Corregido")
    else:
        print(f"  ⏭️  No necesita cambios")

def main():
    print("=" * 80)
    print("🔧 CORRIGIENDO RUTAS EN PÁGINAS HTML")
    print("=" * 80)
    
    if not TEMPLATES_DIR.exists():
        print(f"❌ Error: No existe el directorio {TEMPLATES_DIR}")
        return
    
    for filename in FILES:
        filepath = TEMPLATES_DIR / filename
        if filepath.exists():
            fix_file(filepath)
        else:
            print(f"⚠️  No encontrado: {filepath}")
    
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)

if __name__ == '__main__':
    main()