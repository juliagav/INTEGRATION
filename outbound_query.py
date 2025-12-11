# outbound_query.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import List, Dict
from datetime import datetime

class OutboundQuery:
    """Busca work orders não sincronizadas do MongoDB"""
    
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
            # Testa conexão
            self.client.admin.command('ping')
            self.db = self.client.tractian
            self.collection = self.db.workorders
            print("✅ Conectado ao MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Erro ao conectar no MongoDB: {e}")
            self.client = None
            self.collection = None
    
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