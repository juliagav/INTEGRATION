# service/inbound_service.py
import sys
sys.path.insert(0, '.') # Para garantir que src/ seja encontrado

from src.adapters.client_adapter import ClientAdapter
from src.translators.client_to_tracos import ClientToTracOSTranslator
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Dict
import time


class InboundService:
    """
    Processa fluxo INBOUND: Cliente → TracOS
    
    1. Lê TODOS os arquivos JSON de data/inbound/
    2. Valida cada um
    3. Traduz Cliente → TracOS
    4. Salva no MongoDB
    """
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # segundos
    
    def __init__(self):
        # Conecta com o adapter que lê JSONs
        self.client_adapter = ClientAdapter()
        
        # Conecta com o translator
        self.translator = ClientToTracOSTranslator()
        
        # Conecta com MongoDB (com retry)
        self.client = None
        self.collection = None
        self._connect_with_retry()
    
    def _connect_with_retry(self):
        """Tenta conectar ao MongoDB com retry"""
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(f"🔄 Tentativa {attempt}/{self.MAX_RETRIES} - Conectando ao MongoDB...")
                
                self.client = MongoClient(
                    "mongodb://localhost:27017",
                    serverSelectionTimeoutMS=5000
                )
                self.client.admin.command('ping')
                self.db = self.client.tractian
                self.collection = self.db.workorders
                
                print("✅ Conectado ao MongoDB!")
                return
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                print(f"❌ Tentativa {attempt}/{self.MAX_RETRIES} falhou: {e}")
                
                if attempt < self.MAX_RETRIES:
                    print(f"⏳ Aguardando {self.RETRY_DELAY}s antes de tentar novamente...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    print("❌ Todas as tentativas falharam. MongoDB indisponível.")
    
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
        
        # 1. Lê TODOS os arquivos JSON de data/inbound/
        work_orders = self.client_adapter.read_inbound_files()
        
        if not work_orders:
            print("\n⚠️ Nenhuma work order válida encontrada!")
            return
        
        print(f"\n📋 Processando {len(work_orders)} work orders...\n")
        
        sucesso = 0
        falha = 0
        
        # 2. Para CADA work order lida do JSON
        for client_data in work_orders:
            try:
                # 3. Traduz Cliente → TracOS
                tracos_data = self.translator.translate(client_data)
                print(f"✅ Traduzido: orderNo #{client_data['orderNo']}")
                
                # 4. Salva no MongoDB
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
        if self.client:
            self.client.close()
            print("✅ Conexão MongoDB fechada")


async def main():
    """Teste do serviço inbound"""
    print("="*60)
    print("🧪 TESTE COMPLETO: INBOUND SERVICE")
    print("="*60 + "\n")
    
    service = InboundService()
    service.process()
    service.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())