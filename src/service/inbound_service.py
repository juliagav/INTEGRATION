# src/service/inbound_service.py
import sys
sys.path.insert(0, '.')

from src.adapters.client_adapter import ClientAdapter
from src.translators.client_to_tracos import ClientToTracOSTranslator
from src.database.connection import get_db, get_workorders_collection
from typing import Dict


class InboundService:
    """
    Processa fluxo INBOUND: Cliente → TracOS
    
    1. Lê TODOS os arquivos JSON de data/inbound/
    2. Valida cada um
    3. Traduz Cliente → TracOS
    4. Salva no MongoDB
    """
    
    def __init__(self):
        self.client_adapter = ClientAdapter()
        self.translator = ClientToTracOSTranslator()
        
        # Usa conexão centralizada
        self.db = get_db()
        self.collection = get_workorders_collection()
    
    def save_to_mongodb(self, work_order: Dict) -> bool:
        """Salva work order no MongoDB"""
        if self.collection is None:
            print("❌ Sem conexão com MongoDB")
            return False
        
        try:
            result = self.collection.update_one(
                {"number": work_order["number"]},
                {"$set": work_order},
                upsert=True
            )
            
            if result.upserted_id:
                print(f"✅ Inserida: Work Order #{work_order['number']}")
            else:
                print(f"✅ Atualizada: Work Order #{work_order['number']}")
            return True
        
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False
    
    def process(self):
        """Executa o fluxo INBOUND completo"""
        print("🚀 Iniciando fluxo INBOUND\n")
        
        work_orders = self.client_adapter.read_inbound_files()
        
        if not work_orders:
            print("\n⚠️ Nenhuma work order válida encontrada!")
            return
        
        print(f"\n📋 Processando {len(work_orders)} work orders...\n")
        
        sucesso = 0
        falha = 0
        
        for client_data in work_orders:
            try:
                tracos_data = self.translator.translate(client_data)
                print(f"✅ Traduzido: orderNo #{client_data['orderNo']}")
                
                if self.save_to_mongodb(tracos_data):
                    sucesso += 1
                else:
                    falha += 1
                    
            except Exception as e:
                print(f"❌ Erro ao processar #{client_data.get('orderNo')}: {e}")
                falha += 1
        
        print(f"\n✅ Fluxo INBOUND concluído!")
        print(f"📊 Resultado: {sucesso} sucesso, {falha} falha")
    
    def close(self):
        """Fecha conexão com MongoDB"""
        self.db.close()


if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTE COMPLETO: INBOUND SERVICE")
    print("="*60 + "\n")
    
    service = InboundService()
    service.process()
    service.close()