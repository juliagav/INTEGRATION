from src.database.connection import get_db, get_workorders_collection
from typing import Dict, List


class TracOSAdapter:
    """Conecta e salva dados no MongoDB (TracOS)"""
    
    def __init__(self):
        self.db = get_db()
        self.collection = get_workorders_collection()
    
    def upsert_work_order(self, work_order: Dict) -> bool:
        """Insere ou atualiza work order no MongoDB"""
        if self.collection is None:
            print(" Sem conexão com MongoDB")
            return False
        
        try:
            result = self.collection.update_one(
                {"number": work_order["number"]},
                {"$set": work_order},
                upsert=True
            )
            
            if result.upserted_id:
                print(f" Inserida: Work Order #{work_order['number']}")
            else:
                print(f" Atualizada: Work Order #{work_order['number']}")
            return True
        
        except Exception as e:
            print(f" Erro ao salvar work order #{work_order.get('number')}: {e}")
            return False
    
    def get_all_work_orders(self) -> List[Dict]:
        """Busca todas as work orders do MongoDB"""
        if self.collection is None:
            print(" Sem conexão com MongoDB")
            return []
        
        try:
            return list(self.collection.find())
        except Exception as e:
            print(f" Erro ao buscar work orders: {e}")
            return []
    
    def close(self):
        """Fecha conexão com MongoDB"""
        self.db.close()


if __name__ == "__main__":
    print(" Testando TracOSAdapter\n")
    
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
    
    print(" Inserindo work order...")
    adapter.upsert_work_order(work_order)
    
    print("\n Buscando todas as work orders...")
    all_orders = adapter.get_all_work_orders()
    print(f"Total no banco: {len(all_orders)}")
    
    adapter.close()