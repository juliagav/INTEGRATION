# outbound_query.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import List, Dict
from datetime import datetime
import time  # ← ADICIONAR


class OutboundQuery:
    """Busca work orders não sincronizadas do MongoDB"""
    
    MAX_RETRIES = 3      # ← ADICIONAR
    RETRY_DELAY = 2      # ← ADICIONAR (segundos)
    
    def __init__(self):
        self.client = None
        self.collection = None
        self._connect_with_retry()  # ← MUDAR: chama o método com retry
    
    # ↓ ADICIONAR ESTE MÉTODO INTEIRO ↓
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
                return  # Sucesso, sai do loop
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                print(f"❌ Tentativa {attempt}/{self.MAX_RETRIES} falhou: {e}")
                
                if attempt < self.MAX_RETRIES:
                    print(f"⏳ Aguardando {self.RETRY_DELAY}s antes de tentar novamente...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    print("❌ Todas as tentativas falharam. MongoDB indisponível.")
    
    # ↓ ESTES MÉTODOS CONTINUAM IGUAIS ↓
    def get_unsynced_work_orders(self) -> List[Dict]:
        """Busca work orders com isSynced = false"""
        if self.collection is None:
            print("❌ Sem conexão com MongoDB")
            return []
        
        try:
            unsynced = list(self.collection.find({"isSynced": False}))
            print(f"📊 Encontradas {len(unsynced)} work orders não sincronizadas")
            return unsynced
        
        except Exception as e:
            print(f"❌ Erro ao buscar work orders: {e}")
            return []
    
    def mark_as_synced(self, work_order_number: int) -> bool:
        """Marca work order como sincronizada"""
        if self.collection is None:
            print("❌ Sem conexão com MongoDB")
            return False
        
        try:
            self.collection.update_one(
                {"number": work_order_number},
                {
                    "$set": {
                        "isSynced": True,
                        "syncedAt": datetime.utcnow()
                    }
                }
            )
            print(f"✅ Work Order #{work_order_number} marcada como sincronizada")
            return True
        
        except Exception as e:
            print(f"❌ Erro ao marcar como sincronizada #{work_order_number}: {e}")
            return False
    
    def close(self):
        """Fecha conexão com MongoDB"""
        if self.client:
            self.client.close()
            print("✅ Conexão MongoDB fechada")


async def main():
    """Teste da query outbound"""
    print("🧪 Testando Busca de Work Orders Não Sincronizadas\n")
    
    query = OutboundQuery()
    
    unsynced = query.get_unsynced_work_orders()
    
    if unsynced:
        print(f"\n📋 Work orders não sincronizadas:")
        for wo in unsynced:
            print(f"   - #{wo['number']}: {wo.get('title', 'Sem título')}")
    else:
        print("\n✅ Todas as work orders já estão sincronizadas!")
    
    query.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())