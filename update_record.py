# update_record.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Dict, List

class TracOSAdapter:
    """Conecta e salva dados no MongoDB (TracOS)"""
    
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client.tractian
            self.collection = self.db.workorders
            print("✅ Conectado ao MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Erro ao conectar no MongoDB: {e}")
            self.client = None
            self.collection = None
    
    def upsert_work_order(self, work_order: Dict) -> bool:
        """Insere ou atualiza work order no MongoDB"""
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
            print(f"❌ Erro ao salvar work order #{work_order.get('number')}: {e}")
            return False
    
    def get_all_work_orders(self) -> List[Dict]:
        """Busca todas as work orders do MongoDB"""
        if self.collection is None:
            print("❌ Sem conexão com MongoDB")
            return []
        
        try:
            return list(self.collection.find())
        except Exception as e:
            print(f"❌ Erro ao buscar work orders: {e}")
            return []
    
    def close(self):
        """Fecha conexão com MongoDB"""
        if self.client:
            self.client.close()
            print("✅ Conexão MongoDB fechada")


async def main():
    """Teste do adapter MongoDB"""
    print("🧪 Testando TracOSAdapter\n")
    
    adapter = TracOSAdapter()
    
    work_order = {
        "number": 999,
        "status": "pending",
        "title": "Test work order",
        "description": "Testing MongoDB insert",
        "createdAt": "2024-12-08T10:00:00+00:00",
        "updatedAt": "2024-12-08T11:00:00+00:00",
        "deleted": False,
        "deletedAt": None,
        "isSynced": False,
        "syncedAt": None
    }
    
    print("📥 Inserindo work order...")
    adapter.upsert_work_order(work_order)
    
    print("\n📊 Buscando todas as work orders...")
    all_orders = adapter.get_all_work_orders()
    print(f"Total no banco: {len(all_orders)}")
    
    adapter.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())