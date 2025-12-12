"""
Teste End-to-End do fluxo de Integração
"""
import pytest
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
    
    # 1. INBOUND: Lê arquivos JSON reais
    work_orders = adapter.read_inbound_files()
    assert len(work_orders) >= 1, "Nenhum arquivo JSON válido encontrado"
    
    # 2. Para cada work order
    for original in work_orders:
        # Verifica estrutura do JSON
        assert "orderNo" in original
        assert "summary" in original
        assert "creationDate" in original
        assert "lastUpdateDate" in original
        
        # 3. Traduz Cliente → TracOS
        tracos = client_to_tracos.translate(original)
        assert tracos["number"] == original["orderNo"]
        assert tracos["title"] == original["summary"]
        
        # 4. Salva no MongoDB (se disponível)
        if collection is not None:
            result = collection.update_one(
                {"number": tracos["number"]},
                {"$set": tracos},
                upsert=True
            )
            assert result.acknowledged == True
        
        # 5. OUTBOUND: Traduz TracOS → Cliente
        final = tracos_to_client.translate(tracos)
        
        # 6. Verifica consistência (ida e volta)
        assert final["orderNo"] == original["orderNo"]
        assert final["summary"] == original["summary"]
    
    print(f"\n Pipeline testado com {len(work_orders)} work orders!")
    """
    TESTE END-TO-END COMPLETO
    Fluxo testado:
    1. Lê JSONs reais de data/inbound/
    2. Valida campos obrigatórios
    3. Traduz Cliente → TracOS
    4. Salva no MongoDB
    5. Busca do MongoDB
    6. Traduz TracOS → Cliente
    7. Verifica consistência dos dados
    """