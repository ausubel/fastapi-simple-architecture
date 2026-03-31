"""
Configuración compartida para todos los tests.

Este archivo se ejecuta automáticamente antes de los tests.
"""

import sys
import os

# Agregamos la raíz del proyecto al path para poder importar 'app' y 'main'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
