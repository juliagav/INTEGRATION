"""
Configurações do pytest
Estou usando arquivos reais e conexão real com MongoDB, o `tests/conftest.py` apenas configura o path do projeto.
"""

import sys
import os

# Adiciona a raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))