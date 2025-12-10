# src/adapters/tracos_adapter.py
from pymongo import MongoClient
from typing import Dict, List

class TracOSAdapter:
    """Conecta e salva dados no MongoDB (TracOS)"""
    
    def __init__(self):
        # Conectar no MongoDB (síncrono)
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.tractian
        self.collection = self.db.workorders
    
    def upsert_work_order(self, work_order: Dict) -> None:
        """
        Insere ou atualiza work order no MongoDB
        
        Args:
            work_order: Dados da work order
        """
        # Upsert: atualiza se existir, insere se não existir
        result = self.collection.update_one(
            {"number": work_order["number"]},  # Busca por number
            {"$set": work_order},              # Atualiza/insere
            upsert=True                        # Cria se não existir
        )
        
        if result.upserted_id:
            print(f"✅ Inserida: Work Order #{work_order['number']}")
        else:
            print(f"✅ Atualizada: Work Order #{work_order['number']}")
    
    def get_all_work_orders(self) -> List[Dict]:
        """
        Busca todas as work orders do MongoDB
        
        Returns:
            Lista de work orders
        """
        work_orders = list(self.collection.find())
        return work_orders
    
    def close(self):
        """Fecha conexão com MongoDB"""
        self.client.close()


async def main():
    """Teste do adapter MongoDB"""
    print("🧪 Testando TracOSAdapter\n")
    
    # Criar adapter
    adapter = TracOSAdapter()
    
    # Dados de exemplo (formato TracOS)
    work_order = {
        "number": 999,
        "status": "pending",
        "title": "Test work order",
        "description": "Testing MongoDB insert",
        "createdAt": "2024-12-08T10:00:00+00:00",
        "updatedAt": "2024-12-08T11:00:00+00:00",
        "deleted": False,
        "deletedAt": None
    }
    
    # Inserir
    print("📥 Inserindo work order...")
    adapter.upsert_work_order(work_order)
    
    # Buscar todas
    print("\n📊 Buscando todas as work orders...")
    all_orders = adapter.get_all_work_orders()
    print(f"Total no banco: {len(all_orders)}")
    
    # Mostrar a que acabamos de inserir
    print("\n📄 Work order inserida:")
    import json
    print(json.dumps(work_order, indent=2, default=str))
    
    # Fechar conexão
    adapter.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())