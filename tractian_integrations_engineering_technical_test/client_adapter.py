# src/adapters/client_adapter.py
import json
from pathlib import Path
from typing import List, Dict

class ClientAdapter:
    """Lê e escreve arquivos JSON do sistema do cliente"""
    
    def __init__(self):
        self.inbound_dir = Path("./data/inbound")
        self.outbound_dir = Path("./data/outbound")
    
    def read_inbound_files(self) -> List[Dict]:
        """Lê todos os arquivos JSON da pasta inbound"""
        work_orders = []
        
        # Pega todos os arquivos .json
        json_files = list(self.inbound_dir.glob("*.json"))
        
        print(f" Encontrados {len(json_files)} arquivos JSON")
        
        for file_path in json_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                work_orders.append(data)
                print(f"✅ Lido: {file_path.name}")
        
        return work_orders
    
    def write_outbound_file(self, work_order: Dict) -> None:
        """Escreve uma work order como JSON na pasta outbound"""
        filename = f"{work_order['orderNo']}.json"
        file_path = self.outbound_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(work_order, f, indent=2)
        
        print(f" Escrito: {filename}")


async def main():
    """Teste do adapter"""
    print(" Testando ClientAdapter...\n")
    
    # Criar adapter
    adapter = ClientAdapter()
    
    # Ler JSONs
    work_orders = adapter.read_inbound_files()
    
    # Mostrar resultado
    print(f"\n Total lido: {len(work_orders)} work orders")
    
    if work_orders:
        print("\n Primeira work order:")
        print(json.dumps(work_orders[0], indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
