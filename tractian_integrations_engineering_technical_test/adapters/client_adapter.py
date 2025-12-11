# src/adapters/client_adapter.py
import json
from pathlib import Path
from typing import List, Dict

class ClientAdapter:
    """Lê e escreve arquivos JSON do sistema do cliente"""
    
    REQUIRED_FIELDS = ["orderNo", "summary", "creationDate", "lastUpdateDate"]
    
    def __init__(self):
        self.inbound_dir = Path("./data/inbound")
        self.outbound_dir = Path("./data/outbound")
    
    def validate_work_order(self, work_order: Dict) -> bool:
        """Valida se a work order tem todos os campos obrigatórios"""
        for field in self.REQUIRED_FIELDS:
            if field not in work_order:
                print(f"❌ Campo obrigatório faltando: {field}")
                return False
            
            if work_order[field] is None or work_order[field] == "":
                print(f"❌ Campo obrigatório vazio: {field}")
                return False
        
        print(f"✅ Validação OK para orderNo #{work_order.get('orderNo')}")
        return True
    
    def read_inbound_files(self) -> List[Dict]:
        """Lê todos os arquivos JSON da pasta inbound"""
        work_orders = []
        json_files = list(self.inbound_dir.glob("*.json"))
        
        print(f"📥 Encontrados {len(json_files)} arquivos JSON")
        
        for file_path in json_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if self.validate_work_order(data):
                    work_orders.append(data)
                    print(f"✅ Lido e validado: {file_path.name}")
                else:
                    print(f"⚠️  Arquivo ignorado (inválido): {file_path.name}")
        
        return work_orders
    
    def write_outbound_file(self, work_order: Dict) -> None:
        """Escreve uma work order como JSON na pasta outbound"""
        filename = f"{work_order['orderNo']}.json"
        file_path = self.outbound_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(work_order, f, indent=2)
        
        print(f"✅ Escrito: {filename}")


async def main():
    """Testes de validação"""
    print("🧪 Testando Validação...\n")
    
    adapter = ClientAdapter()
    
    # Teste 1: VÁLIDA
    print("Teste 1: Work order VÁLIDA")
    valid_wo = {
        "orderNo": 1,
        "summary": "Test",
        "creationDate": "2024-12-08T10:00:00Z",
        "lastUpdateDate": "2024-12-08T11:00:00Z"
    }
    result = adapter.validate_work_order(valid_wo)
    print(f"Resultado: {result}\n")
    
    # Teste 2: INVÁLIDA (falta campo)
    print("Teste 2: Work order INVÁLIDA (falta campos)")
    invalid_wo = {
        "orderNo": 2,
        "summary": "Test"
    }
    result = adapter.validate_work_order(invalid_wo)
    print(f"Resultado: {result}\n")
    
    # Teste 3: INVÁLIDA (campo vazio)
    print("Teste 3: Work order INVÁLIDA (campo vazio)")
    empty_wo = {
        "orderNo": 3,
        "summary": "",
        "creationDate": "2024-12-08T10:00:00Z",
        "lastUpdateDate": "2024-12-08T11:00:00Z"
    }
    result = adapter.validate_work_order(empty_wo)
    print(f"Resultado: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())