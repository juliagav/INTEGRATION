from src.database.connection import get_db, get_workorders_collection
from typing import List, Dict
from datetime import datetime


class OutboundQuery:
    
    def __init__(self):
        self.db = get_db()
        self.collection = get_workorders_collection()
    
    def get_unsynced_work_orders(self) -> List[Dict]:
        if self.collection is None:
            print(" Sem conexão com MongoDB")
            return []
        
        try:
            unsynced = list(self.collection.find({"isSynced": False}))
            print(f" Encontradas {len(unsynced)} work orders não sincronizadas")
            return unsynced
        
        except Exception as e:
            print(f" Erro ao buscar work orders: {e}")
            return []
    
    def mark_as_synced(self, work_order_number: int) -> bool:
        if self.collection is None:
            print(" Sem conexão com MongoDB")
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
            print(f" Work Order #{work_order_number} marcada como sincronizada")
            return True
        
        except Exception as e:
            print(f" Erro ao marcar como sincronizada #{work_order_number}: {e}")
            return False
    
    def close(self):
        self.db.close()


if __name__ == "__main__":
    print(" Testando Busca de Work Orders Não Sincronizadas\n")
    
    query = OutboundQuery()
    
    unsynced = query.get_unsynced_work_orders()
    
    if unsynced:
        print(f"\n Work orders não sincronizadas:")
        for wo in unsynced:
            print(f"   - #{wo['number']}: {wo.get('title', 'Sem título')}")
    else:
        print("\n Todas as work orders já estão sincronizadas!")
    
    query.close()