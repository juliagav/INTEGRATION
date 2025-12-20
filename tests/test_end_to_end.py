<<<<<<< HEAD
"""
Teste End-to-End do fluxo de Integração
"""
#import pytest
=======

import pytest
>>>>>>> 559fbfc373304c439ec0cc12cbc2bb09ec03c2d6
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Adiciona raiz do projeto ao path

from src.adapters.client_adapter import ClientAdapter
from src.translators.client_to_tracos import ClientToTracOSTranslator
from src.translators.tracos_to_client import TracOSToClientTranslator
from src.database.connection import get_db, get_workorders_collection

def test_complete_end_to_end_pipeline():
    
    # Setup
    adapter = ClientAdapter()
    client_to_tracos = ClientToTracOSTranslator()
    tracos_to_client = TracOSToClientTranslator()
    collection = get_workorders_collection()
    
    work_orders = adapter.read_inbound_files()
    assert len(work_orders) >= 1, "Nenhum arquivo JSON válido encontrado"
    
    for original in work_orders:
        # Verifica estrutura do JSON
        assert "orderNo" in original
        assert "summary" in original
        assert "creationDate" in original
        assert "lastUpdateDate" in original
        
        tracos = client_to_tracos.translate(original)
        assert tracos["number"] == original["orderNo"]
        assert tracos["title"] == original["summary"]
        
        if collection is not None:
            result = collection.update_one(
                {"number": tracos["number"]},
                {"$set": tracos},
                upsert=True
            )
            assert result.acknowledged == True
        
        final = tracos_to_client.translate(tracos)
        
        assert final["orderNo"] == original["orderNo"]
        assert final["summary"] == original["summary"]
    
    print(f"\n Pipeline testado com {len(work_orders)} work orders!")
